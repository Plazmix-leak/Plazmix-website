import datetime
import json

from flask import make_response
from pydantic import BaseModel, ValidationError

from app.blueprints.api.engine.api_class.method.result import ApiMethodResult
from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.errors.internal import InternalApiError
from app.blueprints.api.engine.errors.permission_denied import PermissionDenied
from app.blueprints.api.engine.errors.unsupported import UnsupportedError
from app.blueprints.api.engine.request import ApiRequest
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.error_code import ErrorType
from app.blueprints.api.engine.types.request import RequestType


class ApiClassMethod:
    def __init__(self, api_cls, method,
                 request_methods=None, blocked_time: datetime.timedelta = None,
                 access_level: ApiAccessLevel = None,
                 request_data_class=None, response_check=None):

        if request_methods is None:
            request_methods = [RequestType.GET]

        self._api_cls = api_cls
        self._method = method
        self._blocked_time = blocked_time
        self._request_methods = request_methods
        self._method_access_level = access_level or self._api_cls.settings().access_level
        self._request_data_class: BaseModel = request_data_class
        self._response_check = response_check

    @property
    def signature(self):
        return f"{self._api_cls.__class__.__name__}_{self._method.__name__}"

    def __call__(self, request: ApiRequest):
        method_check = False
        for method in self._request_methods:
            if request.request_type == method:
                method_check = True
                break

        if method_check is False:
            raise UnsupportedError()

        if self._blocked_time is not None:
            method_information = request.application.get_method_information(method_signature=self.signature)
            method_information.access(self._blocked_time)
            method_information.now_request()

        if self._method_access_level.value > request.application.access_level.value:
            raise PermissionDenied()

        if self._request_data_class is not None:
            try:
                response = self._request_data_class.parse_obj(request.body)
            except ValidationError as e:
                raise ApiDefaultError(comment="There was an error while parsing your data in the request,"
                                              f" please read the documentation and try again. Details: {str(e)}",
                                      error_type=ErrorType.BAD_SYNTAX)
        else:
            response = None

        function_result: ApiMethodResult = self._method(self._api_cls, request=request, query=response)

        if self._response_check is False:
            return function_result

        if isinstance(function_result, ApiMethodResult) is False:
            raise InternalApiError()

        if function_result.request_type != request.request_type:
            raise InternalApiError()

        response = make_response(function_result.get_response())
        response.headers[
            'Method-Cooldown-Seconds'] = self._blocked_time.total_seconds() if self._blocked_time is not None else 0
        response.headers['Content-type'] = "application/json"

        return response
