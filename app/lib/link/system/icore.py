from abc import ABC, abstractmethod


class ICore(ABC):
    @abstractmethod
    def link_control(self, http_method, link):
        pass

    @abstractmethod
    def get_all_owner_link(self, owner_id: str):
        pass

    @abstractmethod
    def create_new_link(self, owner_id: str, real_link: str, redirect_type: str, uri=None, disposable=False):
        pass

    @abstractmethod
    def get_link_from_id(self, link_id: int):
        pass

    @abstractmethod
    def get_link_from_uri(self, uri: str):
        pass
