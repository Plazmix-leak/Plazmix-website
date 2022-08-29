from enum import Enum


class HierarchyEnum(Enum):
    @classmethod
    def get_from_technical_name(cls, technical_name):
        for name, value in cls.__dict__.items():
            try:
                # if '_' in name:
                #     continue
                if value.value.get_technical_name == technical_name:
                    return value
            except AttributeError:
                continue
        return cls.DEFAULT



