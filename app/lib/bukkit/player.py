import datetime
import uuid
from typing import List

from flask import request

from .achievement import AchievementCollection, UserAchievement
from .models import Identifiers, Permissions, Auth, Emails, Skins, Leveling, Joins, Friends, Achievements, Suffixes
from app.lib.cache.helpers import cached_class_function_result
from ..cache import Cache
from .games import BukkitPlayerGame


class BukkitPlayer:
    def __init__(self, uuid: str) -> None:
        self._uuid = uuid

        if Identifiers.get_from_uuid(uuid=self._uuid) is None:
            raise ValueError("unknown player")

    def __set_cached_variable(self, variable, value):
        self._cache.set(variable, value, lifetime=datetime.timedelta(minutes=15))

    @property
    def game(self) -> BukkitPlayerGame:
        return BukkitPlayerGame(self.uuid)

    @property
    def uuid(self):
        return self._uuid

    @property
    @cached_class_function_result("uuid", lifetime=datetime.timedelta(minutes=10))
    def achievements_raw(self):
        raw: Achievements = Achievements.get_from_uuid(self.uuid)
        if not raw:
            return ""
        return raw.achievements

    @property
    @cached_class_function_result("uuid", lifetime=datetime.timedelta(minutes=10))
    def suffix(self):
        suffix: Suffixes = Suffixes.get_from_uuid(self.uuid)
        if suffix is None:
            return None
        return suffix.suffix

    @property
    def achievements(self) -> List[UserAchievement]:
        user_achievements = self.achievements_raw.split()
        result = []

        for global_achievement in AchievementCollection:
            added_status = False

            for user_achievement_data in user_achievements:
                achievement_signature, achievement_level, \
                achievement_received_time_raw = user_achievement_data.split(":")
                if achievement_signature != global_achievement.name:
                    continue
                result.append(UserAchievement(global_achievement=global_achievement,
                                              status=True, level=achievement_level,
                                              received_time=datetime.datetime.fromtimestamp(
                                                  float(achievement_received_time_raw) / 1000)))
                added_status = True
                user_achievements.remove(user_achievement_data)

            if added_status is True:
                continue
            result.append(UserAchievement(global_achievement=global_achievement,
                                          status=False))

        return result

    @property
    @cached_class_function_result("uuid")
    def nickname(self):
        return Identifiers.get_from_uuid(uuid=self._uuid).name

    @property
    @cached_class_function_result("uuid", lifetime=datetime.timedelta(minutes=5))
    def permissions(self):
        perm: Permissions = Permissions.get_from_uuid(self.uuid)
        if perm is None:
            return "DEFAULT".split()
        return perm.privileges

    @property
    def hash_password(self):
        auth: Auth = Auth.get_from_uuid(self.uuid)
        return auth.password

    @property
    @cached_class_function_result("uuid")
    def email(self):
        emails: Emails = Emails.get_from_uuid(self.uuid)
        if emails is None:
            return None
        return emails.email

    @property
    @cached_class_function_result("uuid")
    def ip(self):
        auth: Auth = Auth.get_from_uuid(self.uuid)
        return auth.address

    @property
    @cached_class_function_result("uuid")
    def skin(self):
        r: Skins = Skins.get_from_uuid(self.uuid)
        if r is None:
            return "alex"
        return r.identifier

    @property
    @cached_class_function_result("uuid")
    def level(self):
        r = Leveling.get_from_uuid(self.uuid)
        if r is None:
            return 0
        return r.level

    @property
    @cached_class_function_result("uuid")
    def friends_raw(self):
        r = Friends.get_from_uuid(self.uuid)
        if r is None:
            return []
        return r.friends.split()

    @property
    def last_join(self):
        r = Joins.get_from_uuid(self.uuid)
        if r is None:
            return 1
        return r.online_timestamp

    def set_password(self, new_hash_password):
        auth: Auth = Auth.get_from_uuid(self.uuid)
        if auth is None:
            raise ValueError("unknown player")
        auth.set_new_password(new_hash_password)

    def set_email(self, new_email):
        emails: Emails = Emails.get_from_uuid(self.uuid)

        if emails is None:
            Emails.create_from_uuid(self.uuid, new_email)
        else:
            emails.update_email(new_email)

    def update_permission_groups(self, permission_group_list: str) -> Permissions:
        permission_info: Permissions = Permissions.get_from_uuid(self.uuid)
        if permission_info is None:
            permission_info: Permissions = Permissions.create_new(self.uuid, permission_group_list)
            return permission_info
        permission_info.update_permissions(permission_group_list)
        self.clear_cache()
        return permission_info

    def clear_cache(self):
        cache_client = Cache(f"{self.__class__.__name__}.{self.uuid}")
        cache_client.clear()

    @classmethod
    def get_from_uuid(cls, uuid: str):
        cache = Cache(f"get_from_uuid_{uuid}")
        if cache.exist is False:
            cache.set_global_lifetime(datetime.timedelta(days=10))

        cached_uuid = cache.get("uuid", None)
        if cached_uuid is None:
            ident: Identifiers = Identifiers.get_from_uuid(uuid)

            if ident is None:
                raise ValueError("unknown player")
            cache.set("uuid", ident.identifier)
            return cls(ident.identifier)
        return cls(cached_uuid)

    @classmethod
    def get_from_nickname(cls, nickname: str):
        cache = Cache(f"get_from_nickname_{nickname}")
        if cache.exist is False:
            cache.set_global_lifetime(datetime.timedelta(days=10))

        cached_uuid = cache.get("uuid", None)
        if cached_uuid is None:
            ident: Identifiers = Identifiers.get_from_username(nickname)

            if ident is None:
                raise ValueError("unknown player")
            return cls(ident.identifier)
        return cls(cached_uuid)

    @staticmethod
    def get_users_from_group(group):
        cache = Cache(f"BukkitPlayer.get_perm_group.{group}")
        cached_uuids = cache.get("raw_uuids", None)
        result = []

        if cached_uuids is None:
            raws = Permissions.get_from_group(group)
            cached = []
            for raw in raws:
                cached.append(raw.uuid)
            cache.set("raw_uuids", cached)
            cache.set_global_lifetime(datetime.timedelta(minutes=15))

        cached_uuids = cache.get("raw_uuids", None)
        for uuid in cached_uuids:
            try:
                result.append(BukkitPlayer(uuid))
            except ValueError:
                continue
        return result

    @staticmethod
    def get_players_like_nickname(nickname, page=1, limit=15):
        result = []
        raws: List[Identifiers] = Identifiers.get_from_like_nickname(nickname, page, limit)
        for raw in raws:
            result.append(BukkitPlayer(raw.identifier))
        return result

    @classmethod
    def registration(cls, username: str, password: str):
        new_uuid = uuid.uuid4().hex
        this_uud = Identifiers.get_from_username(username)

        if this_uud is not None:
            raise RuntimeError("Uuid already exist")

        if Identifiers.get_from_uuid(new_uuid) is not None:
            raise RuntimeError("Uuid already exist")

        Identifiers.new(new_uuid, username)
        Auth.new(uuid=new_uuid, address=request.remote_addr, pwd=password)
        return cls(new_uuid)
