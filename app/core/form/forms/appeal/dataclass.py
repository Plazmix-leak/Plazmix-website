from pydantic import BaseModel


class AppealFormDataClass(BaseModel):
    cause: str
    proof: str
    responsibility: str
