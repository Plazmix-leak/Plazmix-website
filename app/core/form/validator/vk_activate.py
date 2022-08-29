from abc import ABC
from typing import List

from app.core.user import User, UserExternalService
from ._interface import IValidator
from ..error.validator import ValidationError


class VKAccountValidator(IValidator, ABC):
    def __call__(self, base, user: User):
        user_external_accounts: List[UserExternalService] = user.ext_services

        valid = False
        for external_service in user_external_accounts:
            if external_service.service_name.lower() == "vk":
                valid = True
                break

        if valid is False:
            raise ValidationError(comment="Привяжите VK к аккаунту!")

        return True
