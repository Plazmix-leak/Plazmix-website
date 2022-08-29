from pydantic import BaseModel


class PaginationResponse(BaseModel):
    current_page: int
    items_in_page: int
    max_page: int


class ResponsePaginateStructure(BaseModel):
    pagination: PaginationResponse
