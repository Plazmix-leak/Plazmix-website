import re

from app.helper.online.collections import OnlineNodesCollection, OnlineCollections
from app.helper.online.enums import ModeCollection


class _OnlineCounterHelperElement:
    def __init__(self, technical_name, collections):
        self.technical_name = technical_name
        self.collections_name = collections
        self.online_count = 0


class OnlineCounterHelper:
    def __init__(self):
        self.__mode_data: dict[str, _OnlineCounterHelperElement] = dict()
        self.__collection_data: dict[str, int] = dict()

        for mode in OnlineNodesCollection:
            self.__mode_data[mode.value.get_technical_name()] = _OnlineCounterHelperElement(
                mode.value.get_technical_name(), [col_mode.value for col_mode in mode.value.get_collections()])

        for collection_type in ModeCollection:
            self.__collection_data[collection_type.value] = 0

    def add(self, service_name, online_count):
        mode = self.__mode_data.get(service_name, None)
        if mode is None:
            raise RuntimeError(f"{service_name} is unknown online service")

        mode.online_count += online_count
        for mode_collection_name in mode.collections_name:
            mode_collection = self.__collection_data.get(mode_collection_name, None)
            if mode_collection is None:
                raise RuntimeError(f"{mode_collection_name} is unknown online collection!")

            self.__collection_data[mode_collection_name] += online_count

    def save_result(self):
        for mode in OnlineNodesCollection:
            mode_raw = self.__mode_data.get(mode.value.get_technical_name())
            mode.value.set_current_online(mode_raw.online_count)

        for collection in OnlineCollections:
            collection_raw = self.__collection_data.get(collection.value.get_technical_name(), 0)
            collection.value.set_current_online(collection_raw)


