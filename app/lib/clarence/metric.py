import datetime

from .counter import MetricCounter
from .day import MetricElement


class Metric:
    def __init__(self, metric_name: str) -> None:
        self._name = f"metric_{metric_name}"

    @property
    def name(self) -> str:
        return self._name

    def get_custom_element(self, custom_name: str) -> MetricElement:
        return MetricElement(self, custom_name)

    def get_day(self, date: datetime.date) -> MetricElement:
        return self.get_custom_element(str(date))

    def today(self) -> MetricElement:
        return self.get_day(datetime.datetime.now().date())

    def yesterday(self) -> MetricElement:
        return self.get_day(datetime.datetime.now().date() - datetime.timedelta(days=1))

    def before_yesterday(self) -> MetricElement:
        return self.get_day(datetime.datetime.now().date() - datetime.timedelta(days=2))

    def get_last_seven_days(self) -> list[MetricElement]:
        result: list[MetricElement] = []
        start_day = datetime.datetime.now().date()

        for day in range(0, 6):
            current_day = (start_day - datetime.timedelta(days=day))
            result.append(self.get_day(current_day))

        result.reverse()
        return result

    def get_past_seven_days(self) -> list[MetricElement]:
        result: list[MetricElement] = []
        start_day = datetime.datetime.now().date()

        for day in range(7, 13):
            current_day = (start_day - datetime.timedelta(days=day))
            result.append(self.get_day(current_day))

        result.reverse()
        return result

    def sync_counter(self, counter: MetricCounter):
        metric_count = counter.get()
        counter.remove_count(metric_count)
        self.today().set(metric_count)
