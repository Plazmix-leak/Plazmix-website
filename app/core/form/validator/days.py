import datetime
from abc import ABC

import humanize

from app.core.user import User
from ..models.answer import FormAnswer
from ..error.validator import ValidationError
from ._interface import IValidator


class ThirtyDaysValidation(IValidator, ABC):
    def __call__(self, base, user: User):
        technical_name = base.technical_name
        if FormAnswer.can_submit(technical_name, user) is False:
            last: FormAnswer = FormAnswer.user_last_answer(technical_name, user)
            _t = humanize.i18n.activate("ru_RU")
            d = humanize.naturalday(last.datetime + datetime.timedelta(days=30))
            raise ValidationError(comment=f"Вы сможете подать эту заявку снова: {d}")
        return True

