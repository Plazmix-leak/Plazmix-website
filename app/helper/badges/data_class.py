from pydantic import BaseModel


class BadgeDataClass(BaseModel):
    technical_name: str
    description: str
