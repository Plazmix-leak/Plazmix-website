from app.blueprints.api.helpers.paginate.response import ResponsePaginateStructure
from app.core.models.news import NewsDataModel


class NewsResponse(ResponsePaginateStructure):
    news: list[NewsDataModel]

