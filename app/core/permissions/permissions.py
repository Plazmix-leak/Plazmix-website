import datetime

from .rules import Rules
from .groups import PermissionGroups
from ...lib.cache import Cache


class Permissions:
    # Доступ к панели
    PANEL_ACCESS = Rules("panel_access", group=PermissionGroups.JUNIOR.value, use_hierarchy=True)
    # Доступ к админке
    ADMIN_ACCESS = Rules("admin_access", group=PermissionGroups.ADMINISTRATOR.value, use_hierarchy=True)
    # Доступ к панели модераторов
    MODERATOR_ACCESS = Rules("moder_panel_access", groups=[PermissionGroups.JUNIOR.value,
                                                           PermissionGroups.MODERATOR.value,
                                                           PermissionGroups.MODERATOR_PLUS.value], use_hierarchy=False)
    # Доступ к просмотру заявок
    APPLICATION_CONTROL = Rules("application_control", group=PermissionGroups.MODERATOR_PLUS.value,
                                use_hierarchy=True)
    # Доступно только овнерам
    OWNER_ACCESS = Rules("owner_only", group=PermissionGroups.OWN.value, use_hierarchy=False)

    # Права
    ADD_MODERATOR_ALERT = Rules("add_moder_alert", group=PermissionGroups.MODERATOR_PLUS.value, use_hierarchy=True)

    USER_CHANGE = Rules("user_change", group=PermissionGroups.DEVELOPER.value, use_hierarchy=True)

    USER_VIEW = Rules("user_view", group=PermissionGroups.MODERATOR.value, use_hierarchy=True)

    TECHNICAL_SUPPORT_ACCESS = Rules("technical_support_access", group=PermissionGroups.MODERATOR_PLUS.value,
                                     use_hierarchy=True)

    MODERATOR_CONTROL = Rules("moderation_control", group=PermissionGroups.MODERATOR_PLUS.value,
                              use_hierarchy=True)

    MODERATOR_FORM_ACCESS = Rules("moderator_from_access", group=PermissionGroups.MODERATOR_PLUS.value,
                                  use_hierarchy=True)

    YOUTUBE_FROM_ACCESS = Rules("youtube_from_access", group=PermissionGroups.ADMINISTRATOR.value,
                                use_hierarchy=True)

    APPEAL_FROM_ACCESS = Rules("appeal_from_access", group=PermissionGroups.MODERATOR_PLUS.value,
                               use_hierarchy=True)

    PAGE_EDIT = Rules("pages_editor", group=PermissionGroups.MODERATOR_PLUS.value,
                      use_hierarchy=True)

    @staticmethod
    def check(rule: Rules, user) -> bool:
        if user is None:
            return False
        cache = Cache(f"Permissions.valid.check.{user.uuid}")

        cached_result = cache.get(str(rule))

        if cached_result is True:
            return cached_result

        cache.set_global_lifetime(datetime.timedelta(minutes=30))
        rule_result = rule(user.all_permission_group)
        cache.set(str(rule), rule_result)
        return rule_result
