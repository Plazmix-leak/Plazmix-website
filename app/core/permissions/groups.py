from app.lib.h_enum import HierarchyEnum, HierarchyType


class PermissionGroups(HierarchyEnum):
    DEFAULT = HierarchyType(0, "DEFAULT", "Игрок", html_color="gray")

    # Донат
    STAR = HierarchyType(1, "STAR", "Star", html_color="#FFAA00")
    COSMO = HierarchyType(2, "COSMO", "Cosmo", html_color="#76ff7a")
    GALAXY = HierarchyType(3, "GALAXY", "Galaxy", html_color="#77dde7")
    UNIVERSE = HierarchyType(4, "UNIVERSE", "UNIVERSE", html_color="#FF55FF")
    LUXURY = HierarchyType(5, "LUXURY", "LUXURY", html_color="#FF5555")

    # Медиа
    YOUTUBE = HierarchyType(6, "YOUTUBE", "YouTube", html_color="#FFAA00")
    YOUTUBE_PLUS = HierarchyType(7, "YOUTUBE_PLUS", "YouTube+", html_color="#FFAA00")

    # Специальные
    TESTER = HierarchyType(8, "TESTER", "QA", html_color="#AAAAAA")

    # Персонал
    ART = HierarchyType(9, "ART", "Дизайнер", html_color="#AA00AA")
    BUILDER = HierarchyType(10, "BUILDER", "Строитель", html_color="#00AA00")
    BUILDER_PLUS = HierarchyType(11, "BUILDER_PLUS", "Ст. Строитель", html_color="#00AA00")
    JUNIOR = HierarchyType(12, "JUNIOR", "Мл. Модератор", html_color="#5555FF")
    MODERATOR = HierarchyType(13, "MODERATOR", "Модератор", html_color="#5555FF")
    MODERATOR_PLUS = HierarchyType(14, "MODERATOR_PLUS", "Ст. Модератор", html_color="#5555FF")

    ASSISTANT = HierarchyType(15, "ASSISTANT", "Помощник", html_color="#AAAAAA")
    DEVELOPER = HierarchyType(16, "DEVELOPER", "Разработчик", html_color="#00AAAA")
    ADMINISTRATOR = HierarchyType(17, "ADMINISTRATOR", "Администратор", html_color="#FF5555")
    OWN = HierarchyType(18, "OWNER", "Владелец", html_color="#AA0000")


MODERATION_GROUPS = [PermissionGroups.MODERATOR_PLUS, PermissionGroups.MODERATOR,
                     PermissionGroups.JUNIOR]

STAFF_GROUPS = [PermissionGroups.OWN, PermissionGroups.ADMINISTRATOR, PermissionGroups.DEVELOPER,
                PermissionGroups.ASSISTANT, PermissionGroups.BUILDER_PLUS,
                PermissionGroups.BUILDER, PermissionGroups.ART]
STAFF_GROUPS.extend(MODERATION_GROUPS)
