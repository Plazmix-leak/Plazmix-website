import datetime
import hashlib
import os
from typing import List

import humanize
from flask import url_for, g
from sqlalchemy import func

from app import db
from app.core.user.data_class.groups import UserGroupsDataClass, DefaultGroupDataClass
from app.core.user.data_class.user import UserDataClass, UserOnlineStatus, ExternalServicesDataCls
from app.core.permissions.groups import PermissionGroups
from app.errors import AuthError
from app.helper.badges import BadgeCollections, Badge
from app.helper.decorators.database import manage_session
from app.lib.bukkit import BukkitPlayer
from app.lib.h_enum import HierarchyType
from .helpers.image import UserImage


def _hash_password(password: str):
    salt = os.getenv("PASS_SALT", None)
    if salt is None:
        return ""

    level_1 = hashlib.sha256(password.encode("utf-8")).hexdigest() + salt
    level_2 = hashlib.sha256(level_1.encode("utf-8")).hexdigest()
    return level_2


class User(db.Model):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    uuid = db.Column(db.String(50), nullable=False, unique=True)
    badges = db.Column(db.JSON)
    money_count = db.Column(db.Integer, default=0, nullable=False)
    block_status = db.Column(db.Boolean, nullable=False, default=0)
    block_comment = db.Column(db.String(600), nullable=True)

    auth_sessions = db.relationship("UserAuthSession", back_populates="user", cascade="all, delete-orphan")
    balance_logs = db.relationship("UserBalanceLog", back_populates="user", cascade="all, delete-orphan")
    password_restore = db.relationship("UserPasswordRestore", back_populates="user", cascade="all, delete-orphan")
    email_edit = db.relationship("EditEmail", back_populates="user", cascade="all, delete-orphan")
    form_answers = db.relationship("FormAnswer", back_populates="user", cascade="all, delete-orphan")
    auth_logs = db.relationship("UserAuthLogs", back_populates="user", cascade="all, delete-orphan")
    oauth_tokens = db.relationship("OauthToken", back_populates="user", cascade="all, delete-orphan")
    oauth_auth_codes = db.relationship("OauthAuthorizationCode", back_populates="user", cascade="all, delete-orphan")
    developer_teams = db.relationship("DeveloperTeamMembers", back_populates="user", cascade="all, delete-orphan")
    ext_services = db.relationship("UserExternalService", back_populates="user", cascade="all, delete-orphan")

    def __eq__(self, other):
        return self.uuid == other.uuid

    def get_user_id(self):
        return self.uuid

    @property
    def data_model(self):
        group_all = []
        for group in self.all_permission_group:
            group_all.append(DefaultGroupDataClass(technical_name=group.get_technical_name, label=group.name))

        user_main_group = self.permission_group
        main_group = DefaultGroupDataClass(technical_name=user_main_group.get_technical_name,
                                           label=user_main_group.name)
        groups = UserGroupsDataClass(main_group=main_group,
                                     groups=group_all)

        online_status, online_comment = self.get_online()
        online = UserOnlineStatus(
            status="ONLINE" if online_status else "OFFLINE",
            comment=online_comment
        )

        ext_accounts = []
        for account in self.ext_services:
            if account.visible is False:
                continue
            data = ExternalServicesDataCls(service_type=account.service_name,
                                           external_account_id=account.user_id_service,
                                           external_account_name=account.user_nickname_service)
            ext_accounts.append(data)

        return UserDataClass(id=self.id, uuid=self.uuid,
                             nickname=self.bukkit.nickname,
                             level=self.bukkit.level,
                             groups=groups,
                             badges=[badge.data_class(self) for badge in self.badges_list],
                             online=online,
                             friends_count=len(self.bukkit.friends_raw),
                             image=self.image.data_class,
                             external_services=ext_accounts,
                             suffix=self.bukkit.suffix)

    @property
    def online_data_model(self):
        online_status, online_comment = self.get_online()
        return UserOnlineStatus(
            status="ONLINE" if online_status else "OFFLINE",
            comment=online_comment
        )

    @property
    def bukkit(self) -> BukkitPlayer:
        return BukkitPlayer(self.uuid)

    @property
    def profile_link(self):
        return url_for("profile.user_profile", user_uuid=self.uuid)

    @property
    def panel_profile_link(self):
        return url_for("panel.user_information", user_uuid=self.uuid)

    @property
    def friends(self):
        r = []
        for friend in self.bukkit.friends_raw:
            try:
                r.append(User.get_from_uuid(friend))
            except ValueError:
                continue
        return r

    @property
    def badges_list(self) -> List[Badge]:
        result = []
        user_raw_badges = self.badges or []

        for badge_raw in user_raw_badges:
            try:
                result.append(BadgeCollections.get_from_technical_name(badge_raw))
            except ValueError:
                continue
        return result

    @badges_list.setter
    def badges_list(self, value: List[Badge]):
        in_base = []
        for badge in value:
            in_base.append(badge.technical_name)

        self.badges = in_base
        db.session.commit()

    @property
    def money(self):
        return self.money_count

    @money.setter
    def money(self, amount: int):
        self.money_count += amount
        db.session.commit()

    @property
    def permission_group(self) -> HierarchyType:

        max_group = PermissionGroups.DEFAULT.value
        for group in self.all_permission_group:
            if group > max_group:
                max_group = group
        return max_group

    @property
    def all_permission_group(self) -> List[HierarchyType]:
        groups_raw = self.bukkit.permissions
        result = []
        for group_raw in groups_raw:
            result.append(PermissionGroups.get_from_technical_name(group_raw).value)
        return result

    @property
    def image(self) -> UserImage:
        return UserImage(self.bukkit.skin)

    def contains_group(self, group):
        all_groups = self.all_permission_group
        group = group.value
        check = False
        for gr in all_groups:
            if group == gr:
                check = True
                break
        return check

    def get_online(self) -> tuple[bool, str]:
        bukkit_status = self.bukkit.last_join

        if bukkit_status == 0:
            return True, "Онлайн"
        elif bukkit_status == 1:
            return False, "Ещё не заходил"

        seconds = bukkit_status / 1000
        dt = datetime.datetime.utcfromtimestamp(seconds)
        humanize.i18n.activate("ru_RU")
        human = humanize.naturaltime(datetime.datetime.now() - dt)
        return False, f"Заходил {human}"

    def get_avatar(self, size=100):
        return f"https://minotar.net/avatar/{self.bukkit.skin}/{size}.png"

    def banned(self, comment: str = None):
        self.block_status = True
        self.block_comment = comment
        db.session.commit()
        from app.task.bukkit_server import banned_user
        banned_user.apply_async(
            kwargs={"user_uuid": self.uuid},
            ignore_result=True)

    def unbanned(self):
        self.block_status = False
        self.block_comment = None
        db.session.commit()
        from app.task.bukkit_server import unban_user
        unban_user.apply_async(
            kwargs={"user_uuid": self.uuid},
            ignore_result=True)

    def edit_password(self, new_password: str, send_notification: bool = True) -> None:
        hash_password = _hash_password(new_password)
        bukkit = self.bukkit
        try:
            bukkit.set_password(hash_password)
        except ValueError:
            raise RuntimeError("Internal error")

        from app.task.email import email_edit_password
        if self.email is None:
            return

        if send_notification:
            email_edit_password.apply_async(
                kwargs={"user_uuid": self.uuid},
                ignore_result=True)

        active_sessions = self.auth_sessions
        for session in active_sessions:
            if g.session == session:
                continue
            session.kill()

    def edit_email(self, new_email):
        self.email = new_email
        db.session.commit()
        self.bukkit.set_email(new_email)

    def chek_password(self, pwd):
        hash_pass = _hash_password(pwd)
        if self.bukkit.hash_password != hash_pass:
            return False
        return True

    def give_permission_group(self, group: PermissionGroups):
        if self.contains_group(group) is True:
            return
        from app.task.bukkit_server import give_group
        give_group.apply_async(
            kwargs={"user_uuid": self.uuid, "group": group.value.get_technical_name})

    def remove_permission_group(self, group: PermissionGroups):
        if self.contains_group(group) is False:
            return
        from app.task.bukkit_server import remove_group
        remove_group.apply_async(
            kwargs={"user_uuid": self.uuid, "group": group.value.get_technical_name})


    @classmethod
    @manage_session("web")
    def login(cls, login, password):
        if "@" in login:
            user = cls.query.filter(cls.email == login).first()
        else:
            user = User.get_from_nickname(login)

        if user is None:
            raise AuthError("Пользователя с такой почтой или ником не найдено!")

        if user.chek_password(password) is False:
            raise AuthError("Пароль неверный!")
        return user

    @classmethod
    def get_from_bukkit(cls, player: BukkitPlayer):
        user = cls.query.filter(cls.uuid == player.uuid).first()
        if user is None:
            user = cls(uuid=player.uuid, email=player.email)
            db.session.add(user)
            db.session.commit()
        return user

    @classmethod
    def get_from_uuid(cls, uuid: str):
        r = cls.query.filter(cls.uuid == uuid).first()

        if r is None:
            player = BukkitPlayer.get_from_uuid(uuid)
            return cls.get_from_bukkit(player)

        return r

    @classmethod
    def get_from_id(cls, identification: int):
        r = cls.query.filter(cls.id == identification).first()
        if r is None:
            raise ValueError("Unknown user")
        return r

    @classmethod
    def get_from_nickname(cls, nickname: str):
        player = BukkitPlayer.get_from_nickname(nickname)
        return User.get_from_bukkit(player)

    @classmethod
    def get_from_email(cls, email):
        r = cls.query.filter(func.lower(cls.email) == func.lower(email)).first()
        if r is None:
            raise ValueError("Unknown user")
        return r

    @staticmethod
    def get_all_user_from_group(group):
        bukkit_players = BukkitPlayer.get_users_from_group(group.value.get_technical_name)
        result = []
        for player in bukkit_players:
            user = User.get_from_bukkit(player)
            if user.permission_group != group.value:
                continue
            result.append(User.get_from_bukkit(player))
        return result

    @staticmethod
    def search_from_nickname(nickname, page=1, limit=15):
        bukkit_players = BukkitPlayer.get_players_like_nickname(nickname, page, limit)
        result = []
        for player in bukkit_players:
            result.append(User.get_from_bukkit(player))
        return result

    @classmethod
    def registration(cls, nickname: str, password: str):
        hash_pwd = _hash_password(password)
        try:
            bukkit = BukkitPlayer.registration(username=nickname, password=hash_pwd)
        except RuntimeError:
            raise AuthError("Пользователь с таким никнеймом уже существует")
        local_user = cls.get_from_bukkit(bukkit)
        return local_user
