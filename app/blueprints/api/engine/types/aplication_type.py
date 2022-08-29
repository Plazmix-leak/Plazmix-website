from app.lib.h_enum import HierarchyEnum, HierarchyType


class ApiAccessLevel(HierarchyEnum):
    NONE = HierarchyType(0, 'none', 'public default access')
    PERSONAL = HierarchyType(1, "personal", "Personal")
    DEFAULT = HierarchyType(2, 'default', 'Default application')
    PARTNER = HierarchyType(3, 'partner', 'Partner application')
    VERIFICATION_PARTNER = HierarchyType(4, 'verification_partner', 'Verification Partner application')
    PRIVATE = HierarchyType(5, 'private', 'All access application')
