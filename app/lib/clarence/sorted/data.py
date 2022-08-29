class SortedData:
    def __init__(self, titles: list[str], values: list[int]):
        if len(titles) != len(values):
            raise RuntimeError("Incorrect sorted data!")
        self._titles = titles
        self._values = values

    @property
    def titles(self) -> list[str]:
        return self._titles

    @property
    def data(self) -> list[int]:
        return self._values

    def slice(self, num: int):
        total_len = len(self._titles)
        start_id = total_len - num

        if start_id < 0:
            start_id = 0

        return SortedData(titles=self._titles[start_id:],
                          values=self._values[start_id:])

    def __repr__(self):
        return f"MetricData(title={self._titles}, values={self._values})"

    __str__ = __repr__
