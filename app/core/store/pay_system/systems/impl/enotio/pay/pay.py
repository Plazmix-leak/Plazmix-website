from app.core.store.pay_system.systems.interfaces.payment import IPayment
from ..helpers import generate_pay_sign
from ..config import Config


class Pay(IPayment):
    def __init__(self, pay_id: int, amount: float,
                 comment: str = "Пополнений баланса Plazmix Wallet"):
        self.pay_id = pay_id
        self.amount = float(amount)
        self.comment = comment
        self.sign = generate_pay_sign(Config.MERCHANT_ID, self.amount, Config.SECRET_WORD_1, self.pay_id)

    def get_pay_url(self) -> str:
        pay_endpoint = Config.PAY_ENDPOINT
        return f"{pay_endpoint}?m={Config.MERCHANT_ID}&oa={self.amount}" \
               f"&o={self.pay_id}&s={self.sign}&cr=RUB&c={self.comment}"
