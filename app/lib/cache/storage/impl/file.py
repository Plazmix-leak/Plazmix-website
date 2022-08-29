import datetime
import json
import os
from abc import ABC

from app.lib.cache.storage.istorage import ICacheStorage

CACHE_STORAGE = os.path.join(os.getcwd(), "cache_storage")


def _check_directory():
    if os.path.exists(CACHE_STORAGE) is False:
        os.mkdir(CACHE_STORAGE)


class FileCacheStorage(ICacheStorage, ABC):
    def __init__(self, namespace):
        _check_directory()
        super(FileCacheStorage, self).__init__(namespace=namespace)

        self.__filepath = os.path.join(CACHE_STORAGE, f"namespace_{self.namespace}.json")
        self.__data = self.__load_file_dump_or_dict()

    def check_freshness(self):
        freshness_time_raw = self.__data.get('__freshness__')
        if freshness_time_raw is None:
            return

        freshness_time = datetime.datetime.fromtimestamp(freshness_time_raw)
        now = datetime.datetime.now()
        if now > freshness_time:
            self.clear()
            return
        return

    def refresh(self):
        try:
            del self.__data
        except AttributeError:
            pass
        self.__data = self.__load_file_dump_or_dict()

    def set_freshness(self, timedelta: datetime.timedelta):
        now = datetime.datetime.now() + timedelta
        timestamp = now.timestamp()
        self.__data['__freshness__'] = timestamp
        self.__dump_in_file()

    def can_created(self) -> bool:
        return os.path.exists(self.__filepath)

    def set(self, variable, value):

        self.__data[variable] = value
        self.__dump_in_file()

    def get(self, variable, default=None):
        return self.__data.get(variable, default)

    def clear(self):
        self.__data = dict()
        os.remove(self.__filepath)

    def __load_file_dump_or_dict(self):
        try:
            with open(self.__filepath, "r") as read_file:
                return json.load(read_file)
        except FileNotFoundError:
            return dict()
        except json.decoder.JSONDecodeError:
            os.remove(self.__filepath)
            print(f"Файл {self.__filepath} был повреждён, поэтому мы его удалили")
            return dict()

    def __dump_in_file(self):
        with open(self.__filepath, "w") as write_file:
            json.dump(self.__data, write_file)
