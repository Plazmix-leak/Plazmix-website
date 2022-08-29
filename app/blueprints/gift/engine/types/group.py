from abc import ABC

from app import ErrorPage
from app.core.permissions.groups import PermissionGroups
from app.helper.simple_page import SimplePage
from .__abstract import AbstractGift
from ..error import GiftActivateError


class GroupGift(AbstractGift, ABC):
    @staticmethod
    def get_technical_name():
        return "group"

    @property
    def result_page(self):
        group_name = self.data.get("group", None)

        if group_name is None:
            return ErrorPage(comment="Упс! Мы встретились с неожиданной ошибкой"
                                     " когда активировали подарок,"
                                     " повторите попытку позже или обратитесь в подержку!")
        group = PermissionGroups.get_from_technical_name(group_name).value
        return SimplePage(page_title="Подарок", title=self.name, icon="fad fa-check fa-7x",
                          comment=f"Вам выдана группа {group.name}",
                          icon_color="#22e02e")

    def activate(self, user):
        from app.task.bukkit_server import give_group
        group_name = self.data.get("group", None)
        if group_name is None:
            raise GiftActivateError()
        give_group.apply_async(
            kwargs={"user_uuid": user.uuid, "group": group_name})
