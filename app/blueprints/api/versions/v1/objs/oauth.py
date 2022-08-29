from abc import ABC

from app.blueprints.api.engine.api_class.interface import IApiClass
from app.blueprints.api.engine.api_class.method.decorator import api_method
from app.blueprints.api.engine.api_class.settings import ApiClassSettings
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.request import RequestType
from app.core.developers.oauth.ext import authorization


class Oauth2(IApiClass, ABC):
    def settings(self) -> ApiClassSettings:
        return ApiClassSettings(access_level=ApiAccessLevel.NONE)

    @api_method(request_methods=[RequestType.POST], response_check=False)
    def accessToken(self, request, query):
        return authorization.create_token_response()

    @api_method(request_methods=[RequestType.POST], response_check=False)
    def revokeToken(self, request, query):
        return authorization.create_endpoint_response('revocation')
