from abc import ABC

from flask import url_for

from app.blueprints.api.engine.api_class.interface import IApiClass
from app.blueprints.api.engine.api_class.method.decorator import api_method
from app.blueprints.api.engine.api_class.method.result import ApiMethodResult
from app.blueprints.api.engine.api_class.settings import ApiClassSettings
from app.blueprints.api.engine.request import ApiRequest
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.request import RequestType
from app.blueprints.api.versions.admin_panel.helper.decorators import check_admin_access
from app.blueprints.api.versions.admin_panel.objs.data_cls import FromInfoRequest
from app.core.form.engine import FormEngine
from app.core.form.engine.answer import BaseFormAnswerController
from app.core.form.status import AnswerStatus
from app.core.user.module import UserAuthSession


class Forms(IApiClass, ABC):
    def settings(self) -> ApiClassSettings:
        return ApiClassSettings(access_level=ApiAccessLevel.NONE)

    @api_method(request_methods=[RequestType.GET], query_data_class=FromInfoRequest)
    @check_admin_access
    def getList(self, request: ApiRequest, query: FromInfoRequest, user_session: UserAuthSession):
        result = []
        base_form = FormEngine.get_from_technical_name(query.form_type)
        answer_list = BaseFormAnswerController(base_form).get_all_forms_in_status(
            AnswerStatus(query.form_status), 500)
        for answer in answer_list:
            result.append({
                "name": f"Заявка от {answer.model.user.bukkit.nickname}",
                "link": f"<a href='{url_for('panel.form_view', answer_id=answer.id)}'"
                        f" class='btn btn-link btn-outline-info' target='_blank'>Открыть</a>"
            })

        return ApiMethodResult(response=result, request_type=RequestType.GET)
