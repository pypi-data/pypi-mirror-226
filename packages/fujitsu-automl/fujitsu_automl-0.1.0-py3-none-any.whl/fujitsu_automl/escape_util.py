import html


def _escape(response):
    response = html.escape(response)
    response = response.replace("(", "\\(")
    response = response.replace(")", "\\)")
    return response


def escape(response):
    if isinstance(response, str):
        return _escape(response)
    elif isinstance(response, list):
        original = list()
        for v in response:
            original.append(escape(v))
        return original
    elif isinstance(response, dict):
        original = dict()
        for k, v in response.items():
            original[_escape(k)] = escape(v)
        return original
    else:
        return response


def _unescape(response):
    response = response.replace("\\)", ")")
    response = response.replace("\\(", "(")
    response = html.unescape(response)
    return response


def unescape(response):
    if isinstance(response, str):
        return _unescape(response)
    elif isinstance(response, list):
        original = list()
        for v in response:
            original.append(unescape(v))
        return original
    elif isinstance(response, dict):
        original = dict()
        for k, v in response.items():
            original[_unescape(k)] = unescape(v)
        return original
    else:
        return response
