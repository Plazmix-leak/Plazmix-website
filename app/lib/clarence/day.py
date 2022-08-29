import datetime

from app.lib.cache import Cache, FileCacheStorage

from ._helpers import get_now_point


class MetricElement:
    def __init__(self, metric, ident: str):
        self._ident = ident.replace(" ", "_")
        self._metric = metric
        self.__cache = Cache(namespace=f"clarence_element_{str(self._ident)}_{self._metric.name}",
                             storage=FileCacheStorage)

    @property
    def line(self):
        return self.__cache.get("line", dict())

    @property
    def last_value(self):
        return self.__cache.get("last_value", 0)

    @last_value.setter
    def last_value(self, value):
        self.__cache.set("last_value", value)

    @property
    def average(self):
        line = self.line
        count = 0
        summa = 0

        for value in line.values():
            count += 1
            summa += value
        try:
            return int(summa/count)
        except ZeroDivisionError:
            return 0

    @property
    def max(self):
        line = self.line
        maximum = 0
        for value in line.values():
            if maximum < value:
                maximum = value
        return maximum

    @property
    def min(self):
        line = self.line
        minimum = int("inf")
        for value in line.values():
            if value < minimum:
                minimum = value
        return minimum

    @property
    def sum(self):
        line = self.line
        res = 0
        for line_element in line.values():
            res += line_element
        return res

    def __update_line(self, point: datetime.datetime, value):
        line = self.__cache.get("line", {})
        line[point.timestamp()] = value
        self.__cache.set("line", line)

    def increment(self, count):
        point = get_now_point()
        value = int(self.last_value) + int(count)
        self.__update_line(point, value)
        self.last_value = value

    def set(self, value):
        self.last_value = value
        self.__update_line(get_now_point(), int(value))
