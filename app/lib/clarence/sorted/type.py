from enum import Enum


class SortType(Enum):
    MINUTES = "minutes"
    HOURS = "hours"
    DAY = "day"


class CheckType(Enum):
    MAX = "max"
    SUM = "sum"
