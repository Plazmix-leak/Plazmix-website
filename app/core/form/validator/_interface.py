from abc import ABC, abstractmethod

from app.core.user import User


class IValidator(ABC):
    @abstractmethod
    def __call__(self, base, user: User):
        pass
