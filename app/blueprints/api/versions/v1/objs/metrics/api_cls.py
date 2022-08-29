from abc import ABC

from app.blueprints.api.engine.api_class.interface import IApiClass
from app.blueprints.api.engine.api_class.method.decorator import api_method
from app.blueprints.api.engine.api_class.method.result import ApiMethodResult
from app.blueprints.api.engine.api_class.settings import ApiClassSettings
from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.request import ApiRequest
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.error_code import ErrorType
from app.blueprints.api.engine.types.request import RequestType
from app.blueprints.api.versions.v1.objs.metrics.data_cls import MetricPublicDataClsRequest, MetricSorterResponse
from app.blueprints.api.versions.v1.objs.metrics.helper import MetricAvailableCollection
from app.lib.clarence.metric import Metric as DataMetric
from app.lib.clarence.sorted.sorter import DataMetricSorted
from app.lib.clarence.sorted.type import SortType


class Metric(IApiClass, ABC):
    def settings(self) -> ApiClassSettings:
        return ApiClassSettings(access_level=ApiAccessLevel.DEFAULT)

    @api_method(request_methods=[RequestType.POST], query_data_class=MetricPublicDataClsRequest)
    def getFromIdentification(self, request: ApiRequest, query: MetricPublicDataClsRequest):
        metric_info: MetricAvailableCollection = MetricAvailableCollection.get_from_name(query.identification)

        if metric_info.value.api_access_level.value > request.application.access_level.value:
            raise ApiDefaultError("you don't have enough rights",
                                  error_type=ErrorType.FORBIDDEN)
        sorter = DataMetricSorted()
        metric = DataMetric(metric_info.name)

        data_slice = -1

        if query.period == "last_hour":
            sorter.add_metric_day(metric.today())
            sort_type = SortType.MINUTES
            data_slice = 60
        elif query.period == "today":
            sorter.add_metric_day(metric.today())
            sort_type = SortType.HOURS
        elif query.period == "yesterday":
            sorter.add_metric_day(metric.yesterday())
            sort_type = SortType.HOURS
        elif query.period == "before_yesterday":
            sorter.add_metric_day(metric.before_yesterday())
            sort_type = SortType.HOURS
        elif query.period == "24hours":
            sorter.add_metric_day(metric.today())
            sorter.add_metric_day(metric.yesterday())
            sort_type = SortType.HOURS
            data_slice = 24
        elif query.period == "week":
            for element in metric.get_last_seven_days():
                sorter.add_metric_day(element)
            sort_type = SortType.DAY
        elif query.period == "past_week":
            for element in metric.get_past_seven_days():
                sorter.add_metric_day(element)
            sort_type = SortType.DAY
        else:
            raise ApiDefaultError("Unknown metric period, available:"
                                  " last_hour, today, yesterday, before_yesterday, 24hours, week, past_week."
                                  f" You passed - {query.period}",
                                  error_type=ErrorType.BAD_SYNTAX)

        sorted_data = sorter(sort_type=sort_type, check_type=metric_info.value.api_access_level)

        if data_slice != -1:
            sorted_data = sorted_data.slice(data_slice)
        return ApiMethodResult(request_type=RequestType.POST,
                               response=MetricSorterResponse(
                                   identification=metric_info.name,
                                   title=sorted_data.titles,
                                   value=sorted_data.data
                               ).dict())
