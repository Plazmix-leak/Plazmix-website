import datetime
from abc import ABC

from app.blueprints.api.engine.api_class.interface import IApiClass
from app.blueprints.api.engine.api_class.method.decorator import api_method
from app.blueprints.api.engine.api_class.method.result import ApiMethodResult
from app.blueprints.api.engine.api_class.settings import ApiClassSettings
from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.request import ApiRequest
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.error_code import ErrorType
from app.blueprints.api.engine.types.request import RequestType
from app.blueprints.api.versions.v1.objs.moderator_alert.data_class.request import ModeratorAlertGetRequest
from app.blueprints.api.versions.v1.objs.user.data_class.request import UserGetRequest
from app.blueprints.api.versions.v1.objs.user.helpers import get_user
from app.core.user import User as Plazmix
from app.core.panel.models import ModeratorAlert as ModeratorAlertModel
from app.core.panel.types import ModeratorAlertType
from app.core.permissions.helpers import check_moderator


class ModeratorAlert(IApiClass, ABC):
    def settings(self) -> ApiClassSettings:
        return ApiClassSettings(access_level=ApiAccessLevel.DEFAULT)

    @api_method(request_methods=[RequestType.POST],
                cooldown=datetime.timedelta(seconds=10), query_data_class=UserGetRequest)
    @get_user
    def getModerator(self, request: ApiRequest, query: UserGetRequest, player: Plazmix):
        if check_moderator(player) is False:
            raise ApiDefaultError(comment=f"User {player.bukkit.nickname} is not a moderator of the project",
                                  error_type=ErrorType.BAD_SYNTAX)

        alerts = ModeratorAlertModel.get_all_to(to=player, alert_type=ModeratorAlertType.WARNING)
        alerts += ModeratorAlertModel.get_all_to(to=player, alert_type=ModeratorAlertType.REPRIMAND)

        return ApiMethodResult(request_type=RequestType.POST,
                               response={"alerts": [alert.data_model.dict() for alert in alerts]})

    @api_method(request_methods=[RequestType.POST],
                cooldown=datetime.timedelta(seconds=5), query_data_class=ModeratorAlertGetRequest)
    def get(self, request: ApiRequest, query: ModeratorAlertGetRequest):
        try:
            alert: ModeratorAlertModel = ModeratorAlertModel.get_from_id(query.alert_id)
        except ValueError:
            raise ApiDefaultError(comment=f"Alert not found",
                                  error_type=ErrorType.NOT_FOUND)
        return ApiMethodResult(request_type=RequestType.POST,
                               response=alert.data_model.dict())





