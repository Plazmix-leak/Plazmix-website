from pydantic import BaseModel

from app.blueprints.api.helpers.paginate.data_class import PaginateDataClass


class NewsRequest(BaseModel):
    paginate: PaginateDataClass


class NewsGetRequest(BaseModel):
    news_id: int
