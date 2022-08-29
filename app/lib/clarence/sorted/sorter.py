import datetime
from typing import Tuple

from app.lib.clarence.day import MetricElement
from app.lib.clarence.sorted.data import SortedData

from .type import SortType, CheckType


class DataMetricSorted:
    def __init__(self):
        self._raw_lines = []

    def add_metric_day(self, metric_day: MetricElement):
        self._raw_lines.extend(metric_day.line.items())

    def get_raw_data(self) -> list[Tuple[float, int]]:
        self._raw_lines.sort(key=lambda element: float(element[0]))
        return self._raw_lines

    def __call__(self, sort_type: SortType, check_type: CheckType = CheckType.MAX) -> SortedData:
        raw_data = self.get_raw_data()
        raw_result: dict[str, int] = {}

        for point, value in raw_data:
            point = float(point)
            if sort_type == SortType.MINUTES:
                current_time = datetime.datetime.fromtimestamp(point).strftime("%d.%m %H:%M")
            elif sort_type == SortType.HOURS:
                current_time = datetime.datetime.fromtimestamp(point).strftime("%d.%m %H")
            elif sort_type == SortType.DAY:
                current_time = datetime.datetime.fromtimestamp(point).strftime("%d.%m")
            else:
                raise RuntimeError("Sort type is not supported")

            current_data = raw_result.get(current_time, None)
            if current_data is None:
                raw_result[current_time] = value
                continue

            if check_type == CheckType.MAX:
                if value > current_data:
                    raw_result[current_time] = value
            elif check_type == CheckType.SUM:
                raw_result[current_time] += value

        return SortedData(titles=list(raw_result.keys()),
                          values=list(raw_result.values()))
