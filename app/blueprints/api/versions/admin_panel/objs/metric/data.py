from pydantic import BaseModel


class MetricApiRequest(BaseModel):
    name: str
    data_type: str = "today"  # last_hour/today/yesterday/before_yesterday/24hours/week/past_week
    check_type: str = "max"  # sum/max


class MetricSorterResponse(BaseModel):
    title: list[str]
    data: list[int]


class MetricApiDataRequest(BaseModel):
    name: str
    day: str = "today"  # today/yesterday


class MetricApiDataResponse(BaseModel):
    max: int
    min: int
    average: int


class MetricComparisonRequest(BaseModel):
    name: str
    data_type: str  # day/week


class MetricComparisonResponse(BaseModel):
    percent: int
    growth: bool
