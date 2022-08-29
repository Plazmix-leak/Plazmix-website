import datetime

from app.lib.cache.storage.istorage import ICacheStorage
from .storage.impl import RedisCacheStorage


class Cache:
    def __init__(self, namespace: str, storage=RedisCacheStorage):
        self.__storage: ICacheStorage = storage(namespace)
        self.__storage.check_freshness()

    @property
    def exist(self) -> bool:
        return self.__storage.can_created()

    def set_global_lifetime(self, timedelta: datetime.timedelta):
        self.set("__create_time__", datetime.datetime.now().timestamp())
        self.__storage.set_freshness(timedelta=timedelta)

    def get(self, variable, default=None):
        return self.__storage.get(variable=variable, default=default)

    def set(self, variable, value):
        self.__storage.set(variable=variable, value=value)

    def clear(self):
        self.__storage.clear()

    def refresh(self):
        self.__storage.refresh()
