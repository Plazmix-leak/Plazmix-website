from abc import ABC

from app.blueprints.api.engine.api_class.interface import IApiClass
from app.blueprints.api.engine.api_class.method.decorator import api_method
from app.blueprints.api.engine.api_class.method.result import ApiMethodResult
from app.blueprints.api.engine.api_class.settings import ApiClassSettings
from app.blueprints.api.engine.request import ApiRequest
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.request import RequestType
from app.helper.online import OnlineCollections, ModeCollection


class Online(IApiClass, ABC):
    def settings(self) -> ApiClassSettings:
        return ApiClassSettings(access_level=ApiAccessLevel.NONE)

    @api_method(request_methods=[RequestType.POST])
    def get(self, request: ApiRequest, query):
        total_online = OnlineCollections.get_from_type(ModeCollection.TOTAL).value
        return ApiMethodResult(request_type=RequestType.POST,
                               response=dict(
                                   online=total_online.get_current_online()
                               ))
