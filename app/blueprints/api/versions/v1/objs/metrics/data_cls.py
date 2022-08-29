from pydantic import BaseModel


class MetricPublicDataClsRequest(BaseModel):
    identification: str
    period: str = "today"  # last_hour/today/yesterday/before_yesterday/24hours/week/past_week


class MetricSorterResponse(BaseModel):
    identification: str
    title: list[str]
    value: list[int]
