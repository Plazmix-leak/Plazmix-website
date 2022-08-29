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


class ModerAdminForm(FlaskForm):
    junior_success = SubmitField('Выдать должность младшего модератора',
                                 render_kw={"class": "btn btn-block btn-success"})
    moderator_success = SubmitField('Выдать должность  модератора',
                                    render_kw={"class": "btn btn-block btn-warning"})


class ModerFormAdmin(AbstractFormAdminHandler, ABC):
    def form_success_handler(self):
        return AdminPanelSimplePage(title="Приниятия нового модератора",
                                    comment=f"Вы собираетесь принять пользователя {self.get_author().bukkit.nickname}"
                                            f" на должность модератора, выберите ниже подходяшую роль",
                                    form=ModerAdminForm(), page_title="Приниятия нового модератора").build()

    def page_handler(self):
        form_success = ModerAdminForm()
        if form_success.validate_on_submit():
            author: User = self.get_author()
            if form_success.junior_success.data:
                author.give_permission_group(PermissionGroups.JUNIOR)
                flash("Заявку успешно принята, пользователю будет выданы соотвествующие права в течении 2 минут",
                      FlashTypes.INFO)
                self._form_answer.model.update_status(AnswerStatus.ACCEPTED,
                                                      "Ваша заявка принята")
                return self.build_page()
            elif form_success.moderator_success.data:
                author.give_permission_group(PermissionGroups.MODERATOR)
                flash("Заявку успешно принята, пользователю будет выданы соотвествующие права в течении 2 минут",
                      FlashTypes.INFO)
                self._form_answer.model.update_status(AnswerStatus.ACCEPTED,
                                                      "Ваша заявка принята")
                return self.build_page()



