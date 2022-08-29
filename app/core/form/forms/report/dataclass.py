from pydantic import BaseModel


class UserReportFormDataClass(BaseModel):
    intruder_nickname: str
    proof: str
    reason: str
