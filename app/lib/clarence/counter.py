from app import redis_client


class MetricCounter:
    def __init__(self, name):
        self.__namespace = f"metric.clarence.{name}"

    def set(self, value: int):
        redis_client.set(self.__namespace, value)

    def add_count(self, count: int = 1):
        redis_client.incr(self.__namespace, count)

    def remove_count(self, count: int = 1):
        redis_client.decr(self.__namespace, count)

    def get(self):
        if redis_client.exists(self.__namespace) is False:
            return 0
        try:
            return redis_client.get(self.__namespace).decode('utf-8')
        except AttributeError:
            return 0
