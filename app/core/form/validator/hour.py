from abc import ABC

from app.core.user import User
from ._interface import IValidator
from ..error.validator import ValidationError
from ..models.answer import FormAnswer


class HourValidation(IValidator, ABC):
    def __call__(self, base, user: User):
        technical_name = base.technical_name
        if FormAnswer.can_submit(technical_name, user, 3600) is False:
            raise ValidationError(comment=f"Вы сможете подать эту заявку снова через час")
        return True

