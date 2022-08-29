from pydantic import BaseModel

from app.blueprints.api.helpers.paginate.data_class import PaginateDataClass


class UserGetRequest(BaseModel):
    uuid: str = None
    id: int = None
    nickname: str = None


class UserAllRequest(BaseModel):
    paginate: PaginateDataClass


class UserGetStaff(BaseModel):
    staff_group: str


class UserGetExternalService(BaseModel):
    service_account_id: str
