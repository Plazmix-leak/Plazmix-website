from abc import ABC, abstractmethod


class IPaySystemClient(ABC):
    @abstractmethod
    def get_balances(self) -> tuple[float, float]: pass