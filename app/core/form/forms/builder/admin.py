from abc import ABC

from flask import flash
from flask_wtf import FlaskForm
from wtforms import SubmitField

from app.core.form.engine.form_admin import AbstractFormAdminHandler
from app.core.form.status import AnswerStatus
from app.core.permissions.groups import PermissionGroups
from app.core.user import User
from app.helper.flash_types import FlashTypes
from app.helper.simple_page.panel import AdminPanelSimplePage


class BuilderAdminForm(FlaskForm):
    builder_success = SubmitField('Выдать должность билдера',
                                  render_kw={"class": "btn btn-block btn-success"})


class BuilderFormAdmin(AbstractFormAdminHandler, ABC):
    def form_success_handler(self):
        return AdminPanelSimplePage(title="Приниятия нового билдера",
                                    comment=f"Вы собираетесь принять пользователя {self.get_author().bukkit.nickname}"
                                            f" на должность билдера, выберите ниже подходяшую роль",
                                    form=BuilderAdminForm(), page_title="Приниятия нового модератора").build()

    def page_handler(self):
        form_success = BuilderAdminForm()
        if form_success.validate_on_submit():
            author: User = self.get_author()
            if form_success.builder_success.data:
                author.give_permission_group(PermissionGroups.BUILDER)
                flash("Заявку успешно принята, пользователю будет выданы соотвествующие права в течении 2 минут",
                      FlashTypes.INFO)
                self._form_answer.model.update_status(AnswerStatus.ACCEPTED,
                                                      "Ваша заявка принята")
                return self.build_page()
