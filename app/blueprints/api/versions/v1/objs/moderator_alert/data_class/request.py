from pydantic import BaseModel


class ModeratorAlertGetRequest(BaseModel):
    alert_id: int
