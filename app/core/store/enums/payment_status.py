from enum import Enum


class PaymentStatus(Enum):
    CREATED = "CREATED"
    PAID = "PAID"

    @staticmethod
    def get_label(status) -> str:
        label_map = {
            PaymentStatus.CREATED: "Ожидает оплаты",
            PaymentStatus.PAID: "Оплачен"
        }
        return label_map.get(status, "Неизвестно")