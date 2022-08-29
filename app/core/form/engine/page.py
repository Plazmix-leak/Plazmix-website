from flask import g, url_for
from flask_wtf import FlaskForm

from app.core.form.error.validator import ValidationError
from app.core.form.models.answer import FormAnswer
from app.helper.simple_page import SimplePage, ErrorPage, GrayPage, PageButton, ButtonType


class FormPage:
    def __init__(self, form_base):
        self.__base = form_base

    def __call__(self):
        validators = self.__base.validators

        for validator in validators:
            try:
                validator(self.__base, g.user)
            except ValidationError as ve:
                return ErrorPage(comment=ve.comment).add_button(
                    PageButton(url=url_for('team.index'), text="Назад", button_type=ButtonType.COLOR_SUCCESS)
                ).add_button(
                    PageButton(url=url_for('main.index'), text="На главную", button_type=ButtonType.COLOR_PRIMARY)
                ).build()

        form: FlaskForm = self.__base.form_cls()
        if form.validate_on_submit():
            data_class_raw = {}
            for element in form:
                data_class_raw[element.short_name] = element.data

            try:
                data_class = self.__base.dataclass(**data_class_raw)
            except Exception:
                return ErrorPage(
                    comment="Возникла неожиданная ошибка во время обработки, пожалуйста свяжитесь с нами").add_button(
                    PageButton(url="https://vk.me/plazmixnetwork",
                               text="Техническая поддержка",
                               button_type=ButtonType.COLOR_WARNING)
                ).build()

            FormAnswer.new(technical_name=self.__base.technical_name, user=g.user, answer_data_cls=data_class)
            return SimplePage(icon="fad fa-check fa-7x", icon_color="#18c10b",
                              comment=f"Вы успешно подали заявку: {self.__base.label}. Вам ответят в течении 72 часов."
                                      f" Также вы можете отслеживать статус своей заявки в специальном разделе",
                              title="Успешно", page_title="Заявка успешно подана").add_button(
                PageButton(url=url_for('profile.applications')
                           , text="Мои заявки", button_type=ButtonType.COLOR_PRIMARY)
            ).build()

        return GrayPage(form=form,
                        comment=self.__base.comment, title=self.__base.label, page_title=self.__base.label).build()
