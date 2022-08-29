from flask import request, render_template

from app.core.form.engine import FormEngine
from app.core.form.engine.answer import BaseFormAnswerController
from app.core.permissions import Permissions, rule_access_check
from app.helper.decorators.web import login_required
from app.helper.simple_page.panel import AdminPanelSimplePage
from ... import panel


@panel.route('/forms/list/<form_type>/<form_admin_status>', methods=['GET'])
@login_required
@rule_access_check(Permissions.TECHNICAL_SUPPORT_ACCESS)
def form_list(form_type: str, form_admin_status: str):
    base_form = FormEngine.get_from_technical_name(form_type)
    return render_template('adminpanel/elements/forms/list.html',
                           base_form=base_form, form_status=form_admin_status)


@panel.route('/forms/view/<int:answer_id>', methods=['GET', 'POST'])
@login_required
@rule_access_check(Permissions.TECHNICAL_SUPPORT_ACCESS)
def form_view(answer_id: int):
    try:
        form = FormEngine.get_from_answer_id(answer_id=answer_id)
    except RuntimeError:
        return AdminPanelSimplePage(title="Ошибка", comment="Ответ не найден",
                                    page_title="Ошибка").build()

    answer = BaseFormAnswerController(form).get_from_id(answer_id)
    admin = form.admin_router(form, answer)

    if request.method.lower() == "post":
        return admin.page_main_handler()
    return admin.build_page()
