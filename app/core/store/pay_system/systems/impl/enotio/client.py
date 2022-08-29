import requests

from app.core.store.pay_system.systems.interfaces.client import IPaySystemClient
from .config import Config
from .error import EnotApiError


class EnotApiClient(IPaySystemClient):
    def __init__(self):
        self.__api_key = Config.API_KEY
        self.__email = Config.EMAIL
        self.__endpoint = Config.API_ENDPOINT

    def __request(self, api_method, request_method="get", params=None) -> dict:
        final_params = {"api_key": self.__api_key, "email": self.__email}
        if params is not None:
            final_params = {**final_params, **params}
        return requests.request(request_method, api_method, params=final_params).json()

    def get_balances(self) -> tuple[float, float]:
        api_result = self.__request("balance")

        if api_result.get("status", "error") == "error":
            raise EnotApiError(api_result.get("message"))

        balance = float(api_result.get("balance", 0))
        frozen_balance = float(api_result.get("balance_freeze", 0))
        return balance, frozen_balance
