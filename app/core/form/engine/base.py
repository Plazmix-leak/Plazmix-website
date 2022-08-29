from app.helper.fileds_check import view_filed
from .page import FormPage
from .answer import BaseFormAnswerController


class FormBase:
    def __init__(self, technical_name, label, comment, form, dataclass, validators, admin_router):
        self._technical_name = technical_name
        self._label = label
        self._comment = comment

        self._validators = validators

        self._form = form
        self._dataclass = dataclass

        self._fields_map = {}

        self._admin_router = admin_router

    def __load_fields(self):
        active_cls = self._form()
        for element in active_cls:
            if view_filed(element) is False:
                continue

            self._fields_map[element.short_name] = element.label

    @property
    def validators(self):
        return self._validators

    @property
    def admin_router(self):
        return self._admin_router

    @property
    def form_cls(self):
        return self._form

    @property
    def dataclass(self):
        return self._dataclass

    @property
    def technical_name(self):
        return self._technical_name

    @property
    def comment(self):
        return self._comment

    @property
    def label(self):
        return self._label

    @property
    def fields_map(self) -> dict[str, str]:
        self.__load_fields()
        return self._fields_map

    @property
    def page(self) -> FormPage:
        return FormPage(self)

    @property
    def answers(self) -> BaseFormAnswerController:
        self.__load_fields()
        return BaseFormAnswerController(self)
