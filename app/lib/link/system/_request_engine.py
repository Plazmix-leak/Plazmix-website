from json import JSONDecodeError

from sentry_sdk import capture_exception

from app.lib.link.error import LinkServerError

import requests


class ShortLinkEngine:
    def __init__(self, api_token, endpoint, api_version="v1"):
        self._api_token = api_token
        self._endpoint = endpoint
        self._api_version = api_version

    def __call__(self, method, body=None, params=None, http_method="post"):
        try:
            req = requests.request(http_method, f"{self._endpoint}/api/{self._api_version}/{method}",
                                   json=body, params=params, headers={"API-TOKEN": self._api_token},
                                   timeout=20)
            return req.json()
        except (JSONDecodeError, requests.HTTPError, requests.ConnectionError) as error:
            capture_exception(error)
            raise LinkServerError()
