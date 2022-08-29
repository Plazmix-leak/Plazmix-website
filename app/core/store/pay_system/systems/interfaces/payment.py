from abc import ABC, abstractmethod


class IPayment(ABC):
    @abstractmethod
    def __init__(self, pay_id: int, amount: float, **kwargs): pass

    @abstractmethod
    def get_pay_url(self) -> str: pass


