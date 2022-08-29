from pydantic import BaseModel


class NodeInformation(BaseModel):
    identification: str
