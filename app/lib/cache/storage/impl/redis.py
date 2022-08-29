import datetime
import json
from abc import ABC
from json import JSONDecodeError

from app import redis_client
from app.lib.cache.storage.istorage import ICacheStorage


class RedisCacheStorage(ICacheStorage, ABC):
    def __init__(self, namespace):
        super(RedisCacheStorage, self).__init__(namespace=namespace)
        self._connector = redis_client

    def refresh(self):
        pass

    def check_freshness(self):
        return

    def set_freshness(self, timedelta: datetime.timedelta):
        self._connector.expire(self.namespace, timedelta)

    def get_all_namespace(self):
        result = self._connector.get(self.namespace)

        if result is None:
            return {}
        try:
            result = json.loads(result.decode('utf-8'))
        except JSONDecodeError:
            self.clear()
            return {}

        return result

    def can_created(self) -> bool:
        return self._connector.exists(self.namespace)

    def get(self, variable, default=None):
        all_namespace = self.get_all_namespace()

        return all_namespace.get(variable, default)

    def set(self, variable, value):
        update_namespace = self.get_all_namespace()
        update_namespace[variable] = value

        self._connector.set(self.namespace, json.dumps(update_namespace).encode('utf-8'))

    def clear(self):
        self._connector.delete(self.namespace)
