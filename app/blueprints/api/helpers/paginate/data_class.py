from pydantic import BaseModel


class PaginateDataClass(BaseModel):
    count_per_page: int = 10
    page: int = 1
