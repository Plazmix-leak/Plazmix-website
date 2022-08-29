from flask import request

from app.core.store.models import Payment
from app.blueprints.event.engine.error import EventResponse, EventError
from app.blueprints.event.engine.listener import EventListener
from app.core.store.pay_system.systems.impl.enotio.data_classes import PayResultDataClass
from app.core.store.pay_system.systems.impl.enotio.pay import Pay, PayResult


class EnotPayHandler(EventListener):
    def post(self):
        raw_data: dict = request.values

        pay_data: PayResultDataClass = PayResultDataClass.parse_obj(raw_data)

        try:
            pay: Payment = Payment.get_from_id(int(pay_data.merchant_id))
        except ValueError:
            raise EventError("Payment not found!")

        payment: Pay = Pay(pay_id=pay.id, amount=pay_data.amount, comment=pay.pay_system_data.get('comment'))

        pay_result = PayResult(pay_data)
        # todo: Переписать проверку платежей
        # if pay_result.check(payment, pay_data.amount) is False:
        #     raise EventError("Fail validation")
        pay.set_paid()
        raise EventResponse("Success")


