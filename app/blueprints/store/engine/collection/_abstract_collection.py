from enum import Enum


class AbstractStoreCollection(Enum):
    @classmethod
    def get_from_technical_name(cls, technical_name: str):
        for element in cls:
            if element.name == technical_name:
                return element
        raise ValueError("Unknown element")

    @classmethod
    def get_final_price(cls, select_product):
        pass



