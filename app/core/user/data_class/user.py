from pydantic import BaseModel

from app.helper.badges.data_class import BadgeDataClass
from .groups import UserGroupsDataClass
from ..helpers.image import UserImageDataClass


class UserOnlineStatus(BaseModel):
    status: str
    comment: str


class ExternalServicesDataCls(BaseModel):
    service_type: str
    external_account_id: str
    external_account_name: str


class UserDataClass(BaseModel):
    id: int
    uuid: str
    nickname: str
    level: int
    suffix: str = None
    groups: UserGroupsDataClass
    friends_count: int
    badges: list[BadgeDataClass]
    online: UserOnlineStatus
    image: UserImageDataClass
    external_services: list[ExternalServicesDataCls]
