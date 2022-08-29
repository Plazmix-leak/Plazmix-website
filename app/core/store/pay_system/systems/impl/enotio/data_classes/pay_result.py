from pydantic import BaseModel, Field


class PayResultDataClass(BaseModel):
    merchant: int
    amount: float
    credited: float
    intid: int
    enot_id: int = Field(alias="intid")
    merchant_id: str
    sign: str
    sign_2: str
    currency: str
    commission: float
