import datetime
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
from app.blueprints.api.helpers.paginate import get_from_paginate
from app.blueprints.api.versions.v1.objs.news.data_class.request import NewsRequest, NewsGetRequest
from app.blueprints.api.versions.v1.objs.news.data_class.response import NewsResponse
from app.core.models.news import News as NewsModel


class News(IApiClass, ABC):
    def settings(self) -> ApiClassSettings:
        return ApiClassSettings(access_level=ApiAccessLevel.DEFAULT)

    @api_method(request_methods=[RequestType.POST],
                query_data_class=NewsRequest, cooldown=datetime.timedelta(seconds=5))
    def all(self, request: ApiRequest, query: NewsRequest):
        new_page, paginate_response = get_from_paginate(NewsModel, query.paginate, page_limit=50)
        res = NewsResponse(pagination=paginate_response, news=new_page)
        return ApiMethodResult(request_type=RequestType.POST, response=res.dict())

    @api_method(request_methods=[RequestType.POST],
                query_data_class=NewsGetRequest, cooldown=datetime.timedelta(seconds=5))
    def get(self, request: ApiRequest, query: NewsGetRequest):
        try:
            news: NewsModel = NewsModel.get_from_id(query.news_id)
        except ValueError:
            raise ApiDefaultError(comment="the news with this ID was not found!", error_type=ErrorType.NOT_FOUND)

        return ApiMethodResult(request_type=RequestType.POST, response=news.data_model.dict())
