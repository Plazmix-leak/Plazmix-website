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
from app.blueprints.api.versions.admin_panel.helper.decorators import check_admin_access
from app.core.user.module import UserAuthSession
from app.lib.clarence.comparison import Comparison
from app.lib.clarence.metric import Metric as DataMetric
from app.lib.clarence.sorted.sorter import DataMetricSorted
from app.lib.clarence.sorted.type import SortType, CheckType
from .data import MetricApiRequest, MetricSorterResponse, MetricApiDataRequest, \
    MetricApiDataResponse, MetricComparisonRequest, MetricComparisonResponse


class Metric(IApiClass, ABC):
    def settings(self) -> ApiClassSettings:
        return ApiClassSettings(access_level=ApiAccessLevel.NONE)

    @api_method(request_methods=[RequestType.POST], query_data_class=MetricApiRequest)
    @check_admin_access
    def sortedData(self, request: ApiRequest, query: MetricApiRequest, user_session: UserAuthSession):
        sorter = DataMetricSorted()
        metric = DataMetric(query.name)
        check_type = CheckType(query.check_type)

        data_slice = -1

        if query.data_type == "last_hour":
            sorter.add_metric_day(metric.today())
            sort_type = SortType.MINUTES
            data_slice = 60
        elif query.data_type == "today":
            sorter.add_metric_day(metric.today())
            sort_type = SortType.HOURS
        elif query.data_type == "yesterday":
            sorter.add_metric_day(metric.yesterday())
            sort_type = SortType.HOURS
        elif query.data_type == "before_yesterday":
            sorter.add_metric_day(metric.before_yesterday())
            sort_type = SortType.HOURS
        elif query.data_type == "24hours":
            sorter.add_metric_day(metric.today())
            sorter.add_metric_day(metric.yesterday())
            sort_type = SortType.HOURS
            data_slice = 24
        elif query.data_type == "week":
            for element in metric.get_last_seven_days():
                sorter.add_metric_day(element)
            sort_type = SortType.DAY
        elif query.data_type == "past_week":
            for element in metric.get_past_seven_days():
                sorter.add_metric_day(element)
            sort_type = SortType.DAY
        else:
            raise ApiDefaultError("Unknown metric type",
                                  error_type=ErrorType.BAD_SYNTAX)

        sorted_data = sorter(sort_type=sort_type, check_type=check_type)

        if data_slice != -1:
            sorted_data = sorted_data.slice(data_slice)

        return ApiMethodResult(response=MetricSorterResponse(title=sorted_data.titles,
                                                             data=sorted_data.data).dict(),
                               request_type=RequestType.POST)

    @api_method(request_methods=[RequestType.POST], query_data_class=MetricApiDataRequest)
    @check_admin_access
    def data(self, request: ApiRequest, query: MetricApiDataRequest, user_session: UserAuthSession):
        metric: DataMetric = DataMetric(query.name)
        if query.day == "today":
            day = metric.today()
        elif query.day == "yesterday":
            day = metric.yesterday()
        elif query.day == "before_yesterday":
            day = metric.before_yesterday()
        else:
            raise ApiDefaultError("Unknown day", error_type=ErrorType.BAD_SYNTAX)

        response = MetricApiDataResponse(
            max=day.max,
            min=day.min,
            average=day.average
        )
        return ApiMethodResult(request_type=RequestType.POST, response=response.dict())

    @api_method(request_methods=[RequestType.POST], query_data_class=MetricComparisonRequest)
    @check_admin_access
    def comparison(self, request: ApiRequest, query: MetricComparisonRequest, user_session: UserAuthSession):
        comparison_data = Comparison()
        metric = DataMetric(query.name)

        if query.data_type == "week":
            comparison_data.add_first(metric.get_last_seven_days())
            comparison_data.add_second(metric.get_past_seven_days())
        elif query.data_type == "day":
            comparison_data.add_first([metric.yesterday()])
            comparison_data.add_second([metric.before_yesterday()])
        else:
            raise ApiDefaultError("Unknown data type", error_type=ErrorType.BAD_SYNTAX)

        percent = comparison_data.get_percentage_growth()
        response = MetricComparisonResponse(percent=percent if percent > 0 else -1 * percent,
                                            growth=True if percent > 0 else False)
        return ApiMethodResult(response=response.dict(), request_type=RequestType.POST)
