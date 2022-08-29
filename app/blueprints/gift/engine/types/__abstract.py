from abc import ABCMeta, abstractmethod

from app.blueprints.gift.engine.specail_author import SpecialAuthor
from app.core.user import User
from ..error import GiftIsNotActiveError
from ..models import UserGift, Gift


class AbstractGift(metaclass=ABCMeta):
    def __init__(self, uuid: str, use_link: bool, active: bool,
                 usage: int, name: str, author_uuid: str, link_usage_limit: int, data: dict):
        self.uuid = uuid
        self.use_link = use_link
        self.active = active
        self.usage = usage
        self.name = name
        self.author_uuid = author_uuid
        self.link_usage_limit = link_usage_limit
        self.data = {} or data

    @property
    def author_info(self) -> tuple[str, any]:
        # link, name
        try:
            special = SpecialAuthor(self.author_uuid)
            return "special", special.value
        except (ValueError, TypeError):
            try:
                user: User = User.get_from_uuid(self.author_uuid)
                return "user", user
            except ValueError:
                pass
        return "special", "Неизвестный"

    def use(self):
        gift = Gift.get_from_uuid(self.uuid)
        gift.new_use()

    @property
    @abstractmethod
    def result_page(self):
        pass

    @staticmethod
    @abstractmethod
    def get_technical_name():
        pass

    @property
    def active_status(self) -> bool:
        if self.active is False:
            return False

        if self.use_link is True and self.usage >= self.link_usage_limit:
            return False
        return True

    def give(self, user: User):
        if self.active_status is False:
            raise GiftIsNotActiveError()

        UserGift.add_gift_in_user(user, self)
        self.use()

    @abstractmethod
    def activate(self, user):
        pass

    @classmethod
    def get_from_model(cls, model):
        return cls(uuid=model.uuid, use_link=model.use_link, active=model.active,
                   usage=model.usage, name=model.name,
                   author_uuid=model.author_uuid, link_usage_limit=model.link_usage_limit,
                   data=model.data)
