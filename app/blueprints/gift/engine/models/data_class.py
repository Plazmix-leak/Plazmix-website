from pydantic import BaseModel


class UserGiftDataClass(BaseModel):
    name: str
    author_name: str
    open: bool
