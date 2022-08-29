from flask import request

from app.blueprints.api.engine.developers.application import DeveloperApplication
from app.blueprints.api.engine.errors.core import ApiCoreError
from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.errors.unsupported import UnsupportedError
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.error_code import ErrorType
from app.blueprints.api.engine.types.request import RequestType


class ApiRequest:
    def __init__(self, api_class: str, api_class_methods, request_type: RequestType,
                 application: DeveloperApplication):
        self.api_class = api_class
        self.api_class_methods = api_class_methods
        self.request_type = request_type
        self.application = application

    @property
    def body(self) -> dict:
        if self.request_type == RequestType.GET:
            return request.args
        elif self.request_type == RequestType.POST:
            return request.get_json(force=True)
        else:
            return {}

    @classmethod
    def generate(cls, signature):
        try:
            api_class, api_class_methods = signature.split('.')
        except (AttributeError, ValueError, IndexError):
            raise ApiCoreError()

        try:
            request_type = RequestType(request.method)
        except (ValueError, AttributeError):
            raise UnsupportedError()

        application_token_raw = request.headers.get('Authorization', None)

        try:
            application_token_type, application_token = application_token_raw.split()
        except (AttributeError, ValueError):
            application_token_type = "unknown"
            application_token = "unknown"

        if application_token_type.lower() == "app-bearer":
            try:
                application = DeveloperApplication.get_from_token(application_token)
            except ValueError:
                raise ApiDefaultError(comment="Unfortunately, we were unable to get the developer's application"
                                              " for this token, please double-check the request"
                                              " headers and try again. If you think this is a bug,"
                                              " please contact us to fix the problem - https://vk.me/plazmixdevs",
                                      error_type=ErrorType.BAD_SYNTAX)
        elif application_token_type.lower() == "bearer":
            application = DeveloperApplication(
                access_level=ApiAccessLevel.PERSONAL,
                uuid="personal", limit=-1)
        else:
            application = DeveloperApplication(
                access_level=ApiAccessLevel.NONE,
                uuid="public", limit=-1)

        return cls(api_class=api_class, api_class_methods=api_class_methods,
                   request_type=request_type, application=application)
