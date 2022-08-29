import datetime
from .achievement import AchievementCollection


class UserAchievement:
    def __init__(self, global_achievement: AchievementCollection, status: bool,
                 level: int = 0, received_time: datetime.datetime = None):
        self._global_achievement = global_achievement
        self._status = status
        self._level = level
        self._date = received_time

    @property
    def can_received(self) -> bool:
        return self._status

    @property
    def level(self):
        return self._level

    @property
    def achievement(self):
        return self._global_achievement

    @property
    def received_time(self) -> datetime.datetime:
        if self.can_received is False:
            raise RuntimeError("Achievements not received")
        return self._date
