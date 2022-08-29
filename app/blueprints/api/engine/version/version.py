from app.blueprints.api.engine.api_class.method.method import ApiClassMethod
from app.blueprints.api.engine.errors.unknown import UnknownMethodOrClassError
from app.blueprints.api.engine.request import ApiRequest


class ApiVersion:
    def __init__(self, name):
        # settings
        self.version_name = name

        self._methods_collection: dict[str, None] = {}

    def register_methods(self, api_class):
        self._methods_collection[api_class.__name__] = api_class()

    def __call__(self, request: ApiRequest):
        method_class = self._methods_collection.get(request.api_class, None)

        if method_class is None:
            raise UnknownMethodOrClassError()

        method = getattr(method_class, request.api_class_methods, None)

        if method is None:
            raise UnknownMethodOrClassError()

        api_method: ApiClassMethod = method()

        if isinstance(api_method, ApiClassMethod) is False:
            raise UnknownMethodOrClassError()
        return api_method(request=request)
