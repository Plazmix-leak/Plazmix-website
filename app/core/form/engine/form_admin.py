from abc import ABC, abstractmethod

from flask import render_template, flash

from app.core.form.engine.answer import BaseFormAnswer
from app.core.form.helper.admin_form import AdminEditDefaultStatus, AdminFailStatusConfirmation
from app.core.form.status import AnswerStatus
from app.helper.flash_types import FlashTypes
from app.helper.simple_page.panel import AdminPanelSimplePage


class AbstractFormAdminHandler(ABC):
    def __init__(self, form, form_answer: BaseFormAnswer):
        self._form = form
        self._form_answer = form_answer

    def get_author(self):
        return self._form_answer.model.user

    def build_page(self):
        answer_author = self.get_author()
        return render_template("adminpanel/elements/form_answer/default.html", author=answer_author,
                               form_answer_controller=self._form_answer, conrol_form=AdminEditDefaultStatus())

    def page_main_handler(self):
        form_edition = AdminEditDefaultStatus()
        fail_form = AdminFailStatusConfirmation()
        if form_edition.validate_on_submit():
            if form_edition.success_button.data:
                return self.form_success_handler()
            elif form_edition.refusal_button.data:
                return AdminPanelSimplePage(title="Отказ по форме",
                                            comment=f"Вы собираетесь дать отказ по форме"
                                                    f" {self._form.technical_name}#{self._form_answer.id}",
                                            form=AdminFailStatusConfirmation()).build()
            elif form_edition.check_button.data:
                self._form_answer.model.update_status(AnswerStatus.CHECK)
                flash("Статус заявки успешно изменён", FlashTypes.INFO)
                return self.build_page()

        if fail_form.validate_on_submit():
            if fail_form.fail_status_submit.data:
                self._form_answer.model.update_status(AnswerStatus.REFUSAL, fail_form.fail_comment.data or
                                                      "Ваша заявка была откланена администратором проекта")
                flash("Статус заявки успешно изменён", FlashTypes.INFO)
                return self.build_page()

        event = self.page_handler()
        if not event:
            return AdminPanelSimplePage(title="Ошибка",
                                        comment="Похоже вы столкнулись с магией :(."
                                                " Системе не удалось определить событие и "
                                                "обработать его, свяжитесь с разработчиком",
                                        page_title="Магия").build()
        return event

    @abstractmethod
    def form_success_handler(self):
        pass

    @abstractmethod
    def page_handler(self):
        pass
