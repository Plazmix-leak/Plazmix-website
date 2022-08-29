from typing import List

from app.lib.h_enum import HierarchyType


class Rules:
    def __init__(self, technical_name: str, group: HierarchyType = None, groups: List[HierarchyType] = None,
                 use_hierarchy: bool = False) -> None:
        self._name = technical_name
        if groups is None:
            self._groups: List[HierarchyType] = [group]
        else:
            self._groups: List[HierarchyType] = groups
        self._use_hierarchy = use_hierarchy

    def __call__(self, groups: List[HierarchyType]) -> bool:
        if self._use_hierarchy is False:
            for access_group in self._groups:
                if access_group in groups:
                    return True
            return False

        minimal_group = self._groups[0]
        for group in self._groups:
            if group < minimal_group:
                minimal_group = group

        value_max_group = groups[0]
        for group in groups:
            if value_max_group < group:
                value_max_group = group

        if minimal_group <= value_max_group:
            return True
        return False

    def __str__(self):
        return self._name

    __repr__ = __str__
