from app.core.store.pay_system.systems.interfaces.payment_check import IPaymentCheck
from ..data_classes import PayResultDataClass
from .pay import Pay
from ..helpers import generate_pay_sign
from ..config import Config


class PayResult(IPaymentCheck):
    def __init__(self, data_class: PayResultDataClass):
        self.data = data_class

    def check(self, pay: Pay, amount) -> bool:
        sign_2 = generate_pay_sign(Config.MERCHANT_ID, amount, Config.SECRET_WORD_2,
                                   self.data.merchant_id)
        if pay.sign != self.data.sign or self.data.sign_2 != sign_2:
            return False
        return True

    @classmethod
    def get_from_raw(cls, data: dict):
        return cls(data_class=PayResultDataClass.parse_obj(data))
