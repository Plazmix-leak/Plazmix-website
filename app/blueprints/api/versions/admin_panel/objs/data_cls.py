from pydantic import BaseModel


class FromInfoRequest(BaseModel):
    form_type: str
    form_status: str


class StaffTypeData(BaseModel):
    cluster: str