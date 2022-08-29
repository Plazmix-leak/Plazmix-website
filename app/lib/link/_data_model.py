from pydantic import BaseModel


class LinkDataModel(BaseModel):
    id: int = None
    uri: str = None
    owner_id: str
    transitions: int = None
    real_link: str
    disposable: bool = False
    active: bool = True
    redirect_type: str = "default"
