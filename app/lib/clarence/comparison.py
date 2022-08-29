from app.lib.clarence.day import MetricElement


def _list_average(array: list[MetricElement]):
    count = 0
    total_average = 0
    for element in array:
        count += 1
        total_average += element.average

    return int(total_average / count)


class Comparison:
    def __init__(self):
        self._first_iter: list[MetricElement] = []
        self._second_iter: list[MetricElement] = []

    @property
    def first_average(self):
        return _list_average(self._first_iter)

    @property
    def second_average(self):
        return _list_average(self._second_iter)

    def add_first(self, elements: list):
        self._first_iter.extend(elements)

    def add_second(self, elements: list):
        self._second_iter.extend(elements)

    def get_percentage_growth(self):
        first_average = self.first_average
        second_average = self.second_average

        try:
            if first_average > second_average:
                return int((first_average / second_average) * 100 - 100)
            return int((second_average / first_average) * 100 - 100) * -1
        except ZeroDivisionError:
            return 0
