from flask import url_for, g

from app.core.user.module import UserBalanceLog
from app.helper.decorators.web import login_required
from app.helper.simple_page import SimplePage, PageButton, ButtonType, ErrorPage
from .. import store, GroupStoreCollection
from ..forms import PaymentWallet


@store.route('/buy/group/<technical_name>', methods=['GET', 'POST'])
@login_required
def buy_group(technical_name: str):
    try:
        group = GroupStoreCollection.get_from_technical_name(technical_name)
    except ValueError:
        return ErrorPage("Продукт не найден!").build()

    final_price = GroupStoreCollection.get_final_price(group.value)
    if final_price == -1:
        return ErrorPage(comment="У вас уже есть группа выше!").build()

    form = PaymentWallet()
    page = SimplePage(title=f"Покупка группы {group.value.name}",
                      comment=f"Вы собираетесь купить группу {group.value.name} за {final_price} руб."
                              f"<center><h6>У вас на балансе сейчас {g.user.money} руб.</h6></center>",
                      icon="fad fa-money-check fa-7x",
                      icon_color="#9932CC",
                      form=form).add_button(PageButton(url_for("profile.wallet"),
                                                       "Пополнить кошелёк",
                                                       button_type=ButtonType.LINK_SUCCESS))

    if form.validate_on_submit():
        if g.user.money < final_price:
            return ErrorPage(comment="Недостаточно средст для покупки, пополните баланс!").add_button(
                PageButton(url_for("profile.wallet"), "Перейти к кошельку", button_type=ButtonType.COLOR_INFO)
            ).build()
        UserBalanceLog.user_money_edit(g.user, final_price*-1, comment=f"Покупка привелегии {group.value.name}")
        group.value.give(g.user)
        return SimplePage(title="Успешно!", comment=f"Поздравляем с приобритенеием группы {group.value.name}."
                                                    f" <p>В течении нескольких минут донат будет выдан,"
                                                    f" после чего вам необходимо перезайти на проект!</p>",
                          icon="fad fa-check fa-7x",
                          icon_color="#008000").build()
    return page.build()

