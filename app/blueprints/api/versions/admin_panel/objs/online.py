from abc import ABC

from app.blueprints.api.engine.api_class.interface import IApiClass
from app.blueprints.api.engine.api_class.method.decorator import api_method
from app.blueprints.api.engine.api_class.method.result import ApiMethodResult
from app.blueprints.api.engine.api_class.settings import ApiClassSettings
from app.blueprints.api.engine.request import ApiRequest
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.request import RequestType
from app.blueprints.api.versions.admin_panel.helper.decorators import check_admin_access
from app.core.user.module.session import UserAuthSession


class Online(IApiClass, ABC):
    def settings(self) -> ApiClassSettings:
        return ApiClassSettings(access_level=ApiAccessLevel.NONE)
    #
    # @api_method(request_methods=[RequestType.POST])
    # @check_admin_access
    # def getLastSevenDays(self, request: ApiRequest, query, user_session: UserAuthSession):
    #     last_seven_days = ServerOnlineHelper().last_days()
    #     result = {
    #         "title": [],
    #         "data": []
    #     }
    #     for day in last_seven_days:
    #         result["title"].append(str(day.day))
    #         result["data"].append(day.get_average())
    #     return ApiMethodResult(response=result, request_type=RequestType.POST)
    #
    # @api_method(request_methods=[RequestType.POST])
    # @check_admin_access
    # def lastDayOnline(self, request: ApiRequest, query, user_session: UserAuthSession):
    #     last_days = ServerOnlineHelper().last_day_grouped_online()
    #     result = {
    #         "title": [],
    #         "data": []
    #     }
    #     for time, data in last_days:
    #         result["title"].append(time)
    #         result["data"].append(data)
    #
    #     return ApiMethodResult(response=result, request_type=RequestType.POST)
