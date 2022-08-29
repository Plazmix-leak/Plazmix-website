import datetime
from abc import ABCMeta, abstractmethod


class ICacheStorage(metaclass=ABCMeta):
    def __init__(self, namespace):
        self.namespace = namespace

    @abstractmethod
    def can_created(self) -> bool:
        pass

    @abstractmethod
    def check_freshness(self):
        pass

    @abstractmethod
    def set_freshness(self, timedelta: datetime.timedelta):
        pass

    @abstractmethod
    def get(self, variable, default=None):
        pass

    @abstractmethod
    def set(self, variable, value):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def refresh(self):
        pass
