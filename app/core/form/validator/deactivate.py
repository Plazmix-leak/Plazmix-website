from abc import ABC

from app.core.user import User
from ._interface import IValidator
from ..error.validator import ValidationError


class DeactivateValidation(IValidator, ABC):
    def __call__(self, base, user: User):
        raise ValidationError("Упс! К сожалению, заявки на этот статус закрыты. "
                              "Следите за нашими соц. сетями, там мы объявим об открытии набора")

