from typing import List, Any

from ._data_model import LinkDataModel
from .system import CORE
from .enums import LinkOwnerType, RedirectType

ALLOWED_SERVERS = ['https://plzm.xyz/', 'https://sl.plazmix.net/']


class ShortLink:
    def __init__(self, model: LinkDataModel, core):
        self.__model = model
        self.__core = core

    # Получит уникальный идентификатор ссылки
    @property
    def id(self) -> int:
        return self.__model.id

    # Получить uti (https://plzm.xyz/URI)
    @property
    def uri(self) -> str:
        return self.__model.uri

    # Pydantic model (тезническое)
    @property
    def data_model(self) -> LinkDataModel:
        return self.__model

    # Активна ли ссылка
    @property
    def active(self) -> bool:
        return self.__model.active

    # список самих ссылок
    @property
    def urls(self) -> List[str]:
        return [f"{variant}/{self.__model.uri}" for variant in ALLOWED_SERVERS]

    # Удалить ссылку
    def delete(self):
        self.__core.link_control('delete', self)

    # Setter статуса
    @active.setter
    def active(self, new_status: bool):
        self.__model.active = new_status
        self.__model = self.__core.link_control('put', self)

    # Получить все ссылки этого владельца
    @classmethod
    def get_all_link_this_owner(cls, owner_type: LinkOwnerType, owner_identification: Any):
        owner_signature = f"{owner_type.value}:{owner_identification}"
        links_data = CORE.get_all_owner_link(owner_signature)
        return [cls(*link_data) for link_data in links_data]

    # Получить ссылку через её id
    @classmethod
    def get_from_id(cls, link_id: int):
        return cls(*CORE.get_link_from_id(link_id))

    # Получить ссылку через её uri
    @classmethod
    def get_from_uri(cls, uri: str):
        return cls(*CORE.get_link_from_uri(uri))

    # Создать ссылку
    @classmethod
    def create_link(cls, owner_type: LinkOwnerType, owner_identification: Any, real_link: str,
                    uri: str = None, disposable: bool = False,
                    redirect_type: RedirectType = RedirectType.DEFAULT):
        owner_signature = f"{owner_type.value}:{owner_identification}"
        return cls(*CORE.create_new_link(owner_signature, real_link, redirect_type.value, uri, disposable))
