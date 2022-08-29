import datetime
from typing import List

from app import redis_client
from app.helper.online.data import ServerOnlineModeDataCls
from app.helper.online.enums import ModeCollection
from app.lib.cache import Cache, FileCacheStorage
from app.lib.clarence.metric import Metric


class ServerOnlineNode:
    def __init__(self, technical_name: str, title: str, collections: List[ModeCollection] = None) -> None:
        self._technical_name = technical_name
        self._title = title
        self._collections = collections or []
        self.__cache = Cache(namespace=f"online_{technical_name}", storage=FileCacheStorage)

        self._collections.append(ModeCollection.TOTAL)

    def get_technical_name(self):
        return self._technical_name

    def get_clarence(self) -> Metric:
        return Metric(f"online_{self._technical_name}")

    def get_collections(self) -> List[ModeCollection]:
        return self._collections

    def get_current_online(self) -> int:
        self.__cache.refresh()
        return self.__cache.get("current_online", 0)

    def get_last_update(self) -> datetime.datetime:
        raw = self.__cache.get("last_update", 0.0)
        return datetime.datetime.fromtimestamp(raw)

    def set_current_online(self, value: int):
        self.__cache.set("current_online", value)
        self.__cache.set("last_update", datetime.datetime.now().timestamp())
        redis_client.set(f"current_online_{self._technical_name}", value)
        self.get_clarence().today().set(value)

    def get_data_cls(self):
        return ServerOnlineModeDataCls(label=self._title,
                                       identification=self._technical_name,
                                       online=self.get_current_online(),
                                       last_update=self.get_last_update().timestamp())
