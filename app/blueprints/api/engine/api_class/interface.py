from abc import ABC, abstractmethod

from app.blueprints.api.engine.api_class.settings import ApiClassSettings


class IApiClass(ABC):
    @abstractmethod
    def settings(self) -> ApiClassSettings: pass

    # Пример метода API
    # @api_method()
    # def get(self, request: ApiRequest) -> ApiMethodResult:
    #     pass
