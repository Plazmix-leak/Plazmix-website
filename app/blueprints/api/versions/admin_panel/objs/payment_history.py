from abc import ABC
from typing import List

from app.blueprints.api.engine.api_class.interface import IApiClass
from app.blueprints.api.engine.api_class.method.decorator import api_method
from app.blueprints.api.engine.api_class.method.result import ApiMethodResult
from app.blueprints.api.engine.api_class.settings import ApiClassSettings
from app.blueprints.api.engine.request import ApiRequest
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.request import RequestType
from app.blueprints.api.versions.admin_panel.helper.decorators import check_admin_access
from app.core.user import UserBalanceLog
from app.core.user.module import UserAuthSession


class PaymentHistory(IApiClass, ABC):
    def settings(self) -> ApiClassSettings:
        return ApiClassSettings(access_level=ApiAccessLevel.NONE)

    @api_method(request_methods=[RequestType.GET])
    @check_admin_access
    def get(self, request: ApiRequest, query, user_session: UserAuthSession):
        logs: List[UserBalanceLog] = UserBalanceLog.get_last(2000)
        r = []
        for log in logs:
            r.append({
                "id": log.id,
                "user": f"<a href='{log.user.panel_profile_link}'>{log.user.bukkit.nickname}</a>",
                "amount": log.amount,
                "comment": log.comment
            })

        return ApiMethodResult(response=r, request_type=RequestType.GET)

