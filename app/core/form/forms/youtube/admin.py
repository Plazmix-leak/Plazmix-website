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


class YTAdminForm(FlaskForm):
    donate = SubmitField('Выдать Galaxy',
                         render_kw={"class": "btn btn-block btn-primary"})
    yt = SubmitField('Выдать YT',
                     render_kw={"class": "btn btn-block btn-success"})
    yt_plus = SubmitField('Выдать YT+',
                          render_kw={"class": "btn btn-block btn-danger"})


class YTFormAdmin(AbstractFormAdminHandler, ABC):
    def form_success_handler(self):
        return AdminPanelSimplePage(title="Приниятие новго медиа",
                                    comment=f"Вы собираетесь принять пользователя {self.get_author().bukkit.nickname}"
                                            f" на должность медиа, выберите ниже подходяшую роль",
                                    form=YTAdminForm(), page_title="Приниятия нового модератора").build()

    def page_handler(self):
        form_success = YTAdminForm()
        if form_success.validate_on_submit():
            author: User = self.get_author()
            if form_success.donate.data:
                author.give_permission_group(PermissionGroups.GALAXY)
                flash("Пользователю будет выданы соотвествующие права в течении 2 минут",
                      FlashTypes.INFO)
                self._form_answer.model.update_status(AnswerStatus.REFUSAL,
                                                      "Ваша заявка была откланена,"
                                                      " но администраторы нашли ваш контент "
                                                      "перспективным и интересным, поэтому вам была"
                                                      " выдана донат-группа, мы надеемся"
                                                      ", что ваш канал в скором времени вырастет и"
                                                      " вы сможете вновь подать заявку на медиа статус"
                                                      " и получить соотвествуюущую группу! Но на данный момент,"
                                                      " к сожалению ваш канал ещё не до конца соотвествует"
                                                      " нашим требованиям")
            if form_success.yt.data:
                author.give_permission_group(PermissionGroups.YOUTUBE)
                flash("Заявка принята, Пользователю будет выданы соотвествующие права в течении 2 минут",
                      FlashTypes.INFO)
                self._form_answer.model.update_status(AnswerStatus.ACCEPTED, "Заявка принята.")

            if form_success.yt_plus.data:
                author.give_permission_group(PermissionGroups.YOUTUBE_PLUS)
                flash("Заявка принята, Пользователю будет выданы соотвествующие права в течении 2 минут",
                      FlashTypes.INFO)
                self._form_answer.model.update_status(AnswerStatus.ACCEPTED, "Заявка принята, выдана роль YT+")

            return self.build_page()
