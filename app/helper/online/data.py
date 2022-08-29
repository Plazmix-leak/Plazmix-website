from typing import List

from pydantic import BaseModel


class ServerOnlineModeDataCls(BaseModel):
    label: str
    identification: str
    last_update: float
    online: int


class ServerOnlineResultDataCls(BaseModel):
    summary: List[ServerOnlineModeDataCls]
    modes: List[ServerOnlineModeDataCls]
