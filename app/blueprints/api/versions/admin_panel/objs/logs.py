from abc import ABC
from typing import List

from app.blueprints.api.engine.api_class.interface import IApiClass
from app.blueprints.api.engine.api_class.method.decorator import api_method
from app.blueprints.api.engine.api_class.method.result import ApiMethodResult
from app.blueprints.api.engine.api_class.settings import ApiClassSettings
from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.request import ApiRequest
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.error_code import ErrorType
from app.blueprints.api.engine.types.request import RequestType
from app.blueprints.api.versions.admin_panel.helper.decorators import check_admin_access
from app.core.user.module import UserAuthLogs
from app.core.user import User
from app.core.user.module import UserAuthSession
from app.core.permissions import Permissions


class Logs(IApiClass, ABC):
    def settings(self) -> ApiClassSettings:
        return ApiClassSettings(access_level=ApiAccessLevel.NONE)

    @api_method(request_methods=[RequestType.GET])
    @check_admin_access
    def getUser(self, request: ApiRequest, query, user_session: UserAuthSession):
        is_moderator = Permissions.check(Permissions.MODERATOR_ACCESS, user_session.user)

        user_uuid = request.body.get('uuid')

        try:
            target: User = User.get_from_uuid(user_uuid)
        except ValueError:
            raise ApiDefaultError("user not found", ErrorType.NOT_FOUND)

        logs: List[UserAuthLogs] = UserAuthLogs.get_from_user(user=target)

        r = []
        for log in logs:
            r.append({
                "id": log.id,
                "datetime": str(log.datetime),
                "ip": log.ip if is_moderator is False else 'Скрыто',
                "location": log.ip_location if is_moderator is False else 'Скрыто',
                "service": log.service
            })

        return ApiMethodResult(response=r, request_type=RequestType.GET)
