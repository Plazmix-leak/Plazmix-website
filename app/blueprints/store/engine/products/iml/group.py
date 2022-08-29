from abc import ABC

from flask import url_for

from app.core.permissions.groups import PermissionGroups
from app.core.user import User
from .._abstract_product import AbstractStoreProduct


class GroupStoreProduct(AbstractStoreProduct, ABC):
    def __init__(self, group: PermissionGroups, **kwargs):
        super(GroupStoreProduct, self).__init__(**kwargs)
        self._group = group

    @property
    def image(self):
        return url_for('static', filename=f'img/donate/{self._image}')

    @property
    def group(self):
        return self._group

    def give(self, user: User):
        from app.task.bukkit_server import give_group
        give_group.apply_async(
            kwargs={"user_uuid": user.uuid, "group": self.group.value.get_technical_name})
