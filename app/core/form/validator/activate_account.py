from abc import ABC
from typing import List

from app.core.user import User, UserExternalService
from ._interface import IValidator
from ..error.validator import ValidationError


class ActiveAccountValidator(IValidator, ABC):
    def __call__(self, base, user: User):
        user_external_accounts: List[UserExternalService] = user.ext_services
        if user.email is None:
            raise ValidationError(comment="К вашему акканту не привязана почта!")

        valid = False
        for external_service in user_external_accounts:
            if external_service.service_name.lower() == "discord":
                valid = True
                break

        if valid is False:
            raise ValidationError(comment="Привяжите Discord к аккаунту!")

        return True
