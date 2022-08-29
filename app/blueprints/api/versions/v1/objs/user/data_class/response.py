from typing import List

from pydantic import BaseModel

from app.blueprints.api.helpers.paginate.response import ResponsePaginateStructure
from app.core.user.data_class.user import UserDataClass


class AllUsersResponse(ResponsePaginateStructure):
    users: list[UserDataClass]


class UserFriendResponse(BaseModel):
    friends: list[UserDataClass]


class UserAchievement(BaseModel):
    technical_name: str
    received: bool
    section: str
    description: str
    received_time: float = None
    level: int


class UserAchievementResponse(BaseModel):
    achievements: List[UserAchievement]
    received_count: int
    total_count: int
