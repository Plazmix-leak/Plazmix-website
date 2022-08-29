from app.core.store.pay_system.systems.impl.enotio import EnotApiClient
from app.core.store.pay_system.systems.impl.enotio.pay import Pay, PayResult
from app.core.store.pay_system.systems.pay_system import PaySystem


class PaySystemList:
    SYSTEMS = [
        PaySystem("Enot.IO", "ENOTIO", Pay, PayResult, EnotApiClient)
    ]

    @classmethod
    def get_from_name(cls, name: str) -> PaySystem:
        for system in cls.SYSTEMS:
            if system.technical_name == name:
                return system
        raise ValueError("Unknown pay system")
