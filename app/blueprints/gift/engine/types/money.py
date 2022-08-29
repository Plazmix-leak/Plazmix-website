from abc import ABC

from app import ErrorPage
from app.helper.simple_page import SimplePage
from .__abstract import AbstractGift
from app.core.user.module import UserBalanceLog
from ..error import GiftActivateError


class MoneyGift(AbstractGift, ABC):
    @staticmethod
    def get_technical_name():
        return "money"

    @property
    def result_page(self):
        amount = self.data.get('amount', None)
        if amount is None:
            return ErrorPage(comment="Упс! Мы встретились с неожиданной ошибкой"
                                     " когда активировали подарок,"
                                     " повторите попытку позже или обратитесь в подержку!")
        return SimplePage(page_title="Подарок", title=self.name, icon="fad fa-check fa-7x",
                          comment=f"Вам выданы моенты в размере - {amount} руб.",
                          icon_color="#22e02e")

    def activate(self, user):
        amount = self.data.get('amount', None)
        if amount is None:
            raise GiftActivateError()
        UserBalanceLog.user_money_edit(user, amount=amount,
                                       comment=f"Активация подарка: '{self.name}'")
