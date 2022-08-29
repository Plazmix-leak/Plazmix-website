from abc import ABC
from typing import List

from flask import url_for

from app.blueprints.api.engine.api_class.interface import IApiClass
from app.blueprints.api.engine.api_class.method.decorator import api_method
from app.blueprints.api.engine.api_class.method.result import ApiMethodResult
from app.blueprints.api.engine.api_class.settings import ApiClassSettings
from app.blueprints.api.engine.request import ApiRequest
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.request import RequestType
from app.blueprints.api.versions.admin_panel.helper.decorators import check_admin_access
from app.blueprints.api.versions.admin_panel.objs.data_cls import StaffTypeData
from app.core.user import User
from app.core.user.module import UserAuthSession
from app.core.permissions.groups import STAFF_GROUPS, PermissionGroups, MODERATION_GROUPS


class Staff(IApiClass, ABC):
    def settings(self) -> ApiClassSettings:
        return ApiClassSettings(access_level=ApiAccessLevel.NONE)

    @api_method(request_methods=[RequestType.POST])
    @check_admin_access
    def get(self, request: ApiRequest, query, user_session: UserAuthSession):
        staffs: List[User] = []
        for staff_group in STAFF_GROUPS:
            staffs.extend(User.get_all_user_from_group(staff_group))

        r = []
        for user_staff in staffs:
            online_status, online_comment = user_staff.get_online()
            group = user_staff.permission_group.name
            r.append({
                "nickname": user_staff.bukkit.nickname,
                "group": group,
                "level": user_staff.bukkit.level,
                "online": 'Онлайн' if online_status else online_comment,
                "action": f"<a target='_blank'"
                          f" href='{url_for('panel.moderation_profile', moderator_uuid=user_staff.uuid)}'>"
                          f"Профиль модератора<a>" if 'Модератор' in group else ''
            })
        return ApiMethodResult(response=r, request_type=RequestType.POST)

    @api_method(request_methods=[RequestType.GET], query_data_class=StaffTypeData)
    @check_admin_access
    def getFromGroups(self, request: ApiRequest, query: StaffTypeData, user_session: UserAuthSession):
        staffs: List[User] = []
        if query.cluster == "mod":
            for group in MODERATION_GROUPS:
                staffs.extend(User.get_all_user_from_group(group))
        elif query.cluster == "build":
            for group in [PermissionGroups.BUILDER, PermissionGroups.BUILDER_PLUS]:
                staffs.extend(User.get_all_user_from_group(group))
        elif query.cluster == "yt":
            for group in [PermissionGroups.YOUTUBE, PermissionGroups.YOUTUBE_PLUS]:
                staffs.extend(User.get_all_user_from_group(group))

        r = []
        for user_staff in staffs:
            online_status, online_comment = user_staff.get_online()
            group = user_staff.permission_group.name
            data = {
                "nickname": user_staff.bukkit.nickname,
                "group": group,
                "level": user_staff.bukkit.level,
                "online": 'Онлайн' if online_status else online_comment,
            }
            if query.cluster == "mod":
                data["action"] = f"<a target='_blank' class='btn btn-link btn-outline-info'" \
                                 f"href='{url_for('panel.moderation_profile', moderator_uuid=user_staff.uuid)}'>" \
                                 f"Профиль модератора</a>"
            else:
                data["action"] = ""

            data["action"] += f"<a target='_blank' class='btn btn-link btn-outline-primary' " \
                              f"href='" \
                              f"{url_for('panel.permission_control', user_uuid=user_staff.uuid, cluster=query.cluster)}" \
                              f"'>Управление</a>"
            r.append(data)

        return ApiMethodResult(response=r, request_type=RequestType.GET)
