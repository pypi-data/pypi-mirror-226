import json
import os
import time
from importlib.metadata import entry_points
from pathlib import Path
from typing import Tuple

import pkg_resources
import requests
import toml
from jsonrpcclient.requests import request_random
from jsonrpcclient.responses import Ok, parse
from sapientml.params import Dataset, Task
from sapientml.util.json_util import JSONEncoder
from sapientml.util.logging import setup_logger
from sapientml_core import SapientMLGenerator

from . import ps_macros
from .anonymize import Anonymizer
from .auth import Authenticator
from .escape_util import unescape
from .params import ErrorParameters, FujitsuAutoMLConfig, Pipeline, ResultParameters, summarize_dataset

model_dir_path_default = Path(__file__).parent / "models"

logger = setup_logger()

pyproject_path = Path(__file__).parents[1] / "pyproject.toml"
if pyproject_path.exists():
    with open(pyproject_path, "r", encoding="utf-8") as f:
        pyproject = toml.load(f)
    SAPIENTML_VERSION = str(pyproject["tool"]["poetry"]["version"])
else:
    SAPIENTML_VERSION = pkg_resources.get_distribution("fujitsu-automl").version

SAPIENTML_AZURE_API = os.environ.get("SAPIENTML_AZURE_API", "https://sapientml.azure-api.net/rpc")


class FujitsuAutoMLGenerator(SapientMLGenerator):
    def __init__(self, **kwargs):
        self.config = FujitsuAutoMLConfig(**kwargs)
        self.config.postinit()
        eps = entry_points(group="sapientml.code_block_generator")
        self.loaddata = eps["loaddata"].load()(**kwargs)
        self.preprocess = eps["preprocess"].load()(**kwargs)

    def generate_code(self, dataset: Dataset, task: Task) -> Tuple[Dataset, list[Pipeline]]:
        df = dataset.training_dataframe
        # Generate the meta-features
        logger.info("Generating meta features ...")
        dataset_summary = summarize_dataset(df, task)  # type: ignore
        if dataset_summary.has_inf_value_targets:
            raise ValueError("Stopped generation because target columns have infinity value.")

        # discard columns with analysis
        # NOTE: The following code modify task.ignore_columns because ignore_columns is the same instance as task.ignore_columns.
        # 1. columns marked as STR_OTHER
        if ps_macros.STR_OTHER in dataset_summary.meta_features_pp:
            undetermined_column_names = dataset_summary.meta_features_pp[ps_macros.STR_OTHER]
            if isinstance(undetermined_column_names, list):
                task.ignore_columns += undetermined_column_names
        del dataset_summary.meta_features_pp[ps_macros.STR_OTHER]
        # 2. columns with all null values
        if ps_macros.ALL_MISSING_PRESENCE in dataset_summary.meta_features_pp:
            column_names_with_all_missing_values = dataset_summary.meta_features_pp[ps_macros.ALL_MISSING_PRESENCE]
            if isinstance(column_names_with_all_missing_values, list):
                task.ignore_columns += column_names_with_all_missing_values
        del dataset_summary.meta_features_pp[ps_macros.ALL_MISSING_PRESENCE]

        url = SAPIENTML_AZURE_API
        auth = Authenticator()
        config = self.config
        config.client_id = auth.get_client_id()
        org_columns = dataset.training_dataframe.columns.tolist()

        ids = set(org_columns) | set(dataset_summary.columns) | set(task.ignore_columns)
        if config.id_columns_for_prediction is not None:
            ids |= set(config.id_columns_for_prediction)
        # ids.add(dataset.training_data_path)
        # if dataset.validation_data_path:
        #     ids.add(dataset.validation_data_path)
        # if dataset.test_data_path:
        #     ids.add(dataset.test_data_path)
        # if task.split_column_name:
        #     ids.add(task.split_column_name)
        if config.use_word_list:
            ids |= set(config.use_word_list.keys() if isinstance(config.use_word_list, dict) else config.use_word_list)
        # if dataset_summary.cols_numeric_and_string:
        #     ids |= set(dataset_summary.cols_numeric_and_string)
        # if dataset_summary.cols_Japanese_text:
        #     ids |= set(dataset_summary.cols_Japanese_text)
        if dataset_summary.cols_almost_missing_string:
            ids |= set(dataset_summary.cols_almost_missing_string)
        if dataset_summary.cols_almost_missing_numeric:
            ids |= set(dataset_summary.cols_almost_missing_numeric)
        # if dataset_summary.cols_has_symbols:
        #     ids |= set(dataset_summary.cols_has_symbols)
        # if dataset_summary.cols_iterable_values:
        #     ids |= set(dataset_summary.cols_iterable_values)
        anonymizer = Anonymizer(ids)
        task = anonymizer.anonymize(task)  # type: ignore
        dataset_summary = anonymizer.anonymize(dataset_summary)
        config = anonymizer.anonymize(config)

        _params = {
            "version": SAPIENTML_VERSION,
            "task": task.dict(),
            "dataset_summary": dataset_summary.dict(),
            "config": config.dict(),
        }

        # if dry_run:
        #     with open("request_parameters.json", "w") as f:
        #         f.write(json.dumps(_params))

        #     logger.info("request parameters is dumped in ./request_parameters.json")

        #     sys.exit(0)

        logger.info("Calling WebAPIs for generating pipelines ...")
        token = auth.acquire_token()
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.post(
                url,
                data=json.dumps(request_random("register", params=_params), cls=JSONEncoder),  # type: ignore
                timeout=100,
                headers=headers,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            message = f"JSONRPC request failed(method: register): {e}\nparams = {_params}"
            raise RuntimeError(message) from e

        parsed = parse(response.json())

        if isinstance(parsed, Ok):
            uuid = parsed.result["uuid"]
            logger.info(f"Experiment Id: {uuid}")
        else:
            message = f"JSONRPC returns error(method: register): {parsed.message}"  # type: ignore
            raise RuntimeError(message)

        for i in range(100):
            time.sleep(1)
            _params = {
                "version": SAPIENTML_VERSION,
                "uuid": uuid,
            }
            try:
                response = requests.post(
                    url,
                    json=request_random("get_result", params=_params),
                    timeout=100,
                    headers=headers,
                )
                response.raise_for_status()

            except requests.exceptions.RequestException as e:
                message = f"JSONRPC request failed(method: get_result): {e}"
                raise RuntimeError(message) from e

            parsed = parse(response.json())

            if isinstance(parsed, Ok):
                status = parsed.result["status"]
                if status == "Succeeded":
                    break
                elif status == "Failed":
                    error_json = parsed.result["error"]
                    error_json = unescape(error_json)
                    error = ErrorParameters.parse_obj(error_json)
                    error = anonymizer.deanonymize(error)
                    message = f"Error occurred in version {error.version}: {error.message}"  # type: ignore
                    raise RuntimeError(version=error.version, message=error.message)  # type: ignore
            else:
                message = f"JSONRPC returns error(method: get_result): {parsed.message}"  # type: ignore
                raise RuntimeError(message)

        if parsed.result["status"] != "Succeeded":
            raise RuntimeError("Could not get a successful response until 100 retries.")

        try:
            result_json = parsed.result["result"]
            result_json = unescape(result_json)
            result = ResultParameters.parse_obj(result_json)
            result = anonymizer.deanonymize(result)
        except Exception as e:
            message = f"Convert Error(from dict to dataclass): {e}"
            raise RuntimeError(message)

        return dataset, result.pipelines  # type: ignore
