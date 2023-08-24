import json
import logging
import os

import msal
from sapientml.common.exception import SapientMLCoreException
from sapientml.common.internal_path import sapientml_root

logger = logging.getLogger("sapientml")

AUTHORITY = "https://login.microsoftonline.com/8d1a0de1-40c4-4040-9748-a9a2b66d0c2f"
DEFAULT_CLIENT_ID = "7ee0604e-aba1-437a-bf93-2fc3c50500d0"


class Authenticator:
    def __init__(self):
        CLIENT_ID = os.environ.get("SAPIENTML_CLIENT_ID", DEFAULT_CLIENT_ID)
        CLIENT_SECRET = os.environ.get("SAPIENTML_CLIENT_SECRET")
        self._CLIENT_ID = CLIENT_ID

        if CLIENT_SECRET is not None:
            self.app = msal.ConfidentialClientApplication(
                CLIENT_ID,
                authority=AUTHORITY,
                client_credential=CLIENT_SECRET,
            )
            self.SCOPE = ["api://b4ba1dba-4dd4-4948-9ff9-ea7bca4b07f9/.default"]
            self.cache_path = None
        else:
            self.cache = msal.SerializableTokenCache()
            self.cache_path = sapientml_root / "cache.bin"
            if os.path.exists(self.cache_path):
                self.cache.deserialize(open(self.cache_path, "r").read())

            self.app = msal.PublicClientApplication(
                CLIENT_ID,
                authority=AUTHORITY,
                token_cache=self.cache,
            )
            self.SCOPE = ["api://b4ba1dba-4dd4-4948-9ff9-ea7bca4b07f9/RPC.Read"]

    def _acquire_token_for_client(self) -> dict:
        assert isinstance(self.app, msal.ConfidentialClientApplication)

        logger.info("Authenticating app via OAuth 2.0 Client Credentials Flow")

        return self.app.acquire_token_for_client(scopes=self.SCOPE)

    def _acquire_token_for_device(self) -> dict:
        assert isinstance(self.app, msal.PublicClientApplication)

        logger.info("Authenticating app via OAuth 2.0 Device Code Flow")

        accounts = self.app.get_accounts()
        if accounts:
            logger.info(f'Using the cached token of {accounts[0]["username"]}')
            chosen = accounts[0]
            return self.app.acquire_token_silent(
                self.SCOPE,
                account=chosen,
            )  # type: ignore

        flow = self.app.initiate_device_flow(scopes=self.SCOPE)
        if "user_code" not in flow:
            raise ValueError(f"Fail to create device flow. Error: {json.dumps(flow, indent=4)}")

        logger.warn(
            f"""
**********************************************************************

{flow["message"]}

**********************************************************************
"""
        )

        result = self.app.acquire_token_by_device_flow(flow)

        if self.cache.has_state_changed and self.cache_path is not None:
            with open(self.cache_path, "w") as f:
                f.write(self.cache.serialize())

        return result

    def acquire_token(self) -> str:
        if isinstance(self.app, msal.ConfidentialClientApplication):
            result = self._acquire_token_for_client()
        else:
            result = self._acquire_token_for_device()

        if "access_token" in result:
            return result["access_token"]

        raise SapientMLCoreException(
            f'{result.get("error")}\n{result.get("error_description")}\n{result.get("correlation_id")}'
        )

    def get_client_id(self) -> str:
        return self._CLIENT_ID
