from abc import ABC, abstractmethod


class IPaymentCheck(ABC):

    @abstractmethod
    def check(self, pay, amount) -> bool: pass

    @classmethod
    @abstractmethod
    def get_from_raw(cls, data: dict): pass
