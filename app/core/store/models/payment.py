import datetime

from flask import flash, url_for

from app import db
from app.core.store.enums.payment_status import PaymentStatus
from app.core.store.pay_system.list import PaySystemList
from app.core.user import User, UserBalanceLog
from app.helper.flash_types import FlashTypes


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    amount = db.Column(db.Float, default=0, nullable=False)
    pay_system_name = db.Column(db.Enum("ENOTIO", "UNKNOWN"), default="UNKNOWN")
    pay_system_data = db.Column(db.JSON)

    useful_data = db.Column(db.JSON)
    paid_data = db.Column(db.String(600))

    create_datetime = db.Column(db.DateTime, default=datetime.datetime.now())
    paid_datetime = db.Column(db.DateTime)

    status = db.Column(db.Enum("CREATE", "PAID"), default="CREATE")

    ip = db.Column(db.String(50))
    location = db.Column(db.String(200), nullable=True)

    @property
    def current_status(self):
        return PaymentStatus(self.status)

    def set_paid(self):
        if self.status == "PAID":
            return
        self.status = "PAID"
        self.paid_datetime = datetime.datetime.now()
        db.session.commit()
        user_uuid = self.useful_data.get("user_uuid")
        user_wallet_amount = self.useful_data.get("wallet_amount")
        user = User.get_from_uuid(user_uuid)
        UserBalanceLog.user_money_edit(user=user, amount=user_wallet_amount,
                                       comment=f"Пополнение через ENOT.IO на {user_wallet_amount} руб.")

    @property
    def link(self):
        try:
            pay_system = PaySystemList.get_from_name(self.pay_system_name)
        except ValueError:
            flash("Ошибка при генерации платежа, обратитесь к администратору!", FlashTypes.ERROR)
            return url_for("main.index")

        pay_cls = pay_system.payment_cls
        pay_data = self.pay_system_data or {}

        pay = pay_cls(self.id, self.amount, **pay_data)
        return pay.get_pay_url()

    @classmethod
    def create_pay(cls, amount, pay_system, payment_system_data=None, useful_data=None):
        payment_system_data = payment_system_data or {}
        useful_data = useful_data or {}
        new = cls(pay_system_name=pay_system, amount=amount, useful_data=useful_data,
                  pay_system_data=payment_system_data)
        db.session.add(new)
        db.session.commit()
        return new

    @classmethod
    def get_from_id(cls, identification: int):
        r = cls.query.filter(cls.id == identification).first()
        if r is None:
            raise ValueError("Unknown payment")
        return r
