from flask import g, render_template, redirect, flash

from app.core.user.module import UserBalanceLog
from app.core.form.engine import FormEngine
from app.core.form.models.answer import FormAnswer
from app.core.user import User
from app.core.store.models import Payment
from app.helper.decorators.web import login_required
from app.helper.flash_types import FlashTypes
from .. import profile
from ..forms import WalletReplenishForm, WalletTransferForm


@profile.route('/wallet', methods=['GET', 'POST'])
@login_required
def wallet():
    replenish_from = WalletReplenishForm()
    transfer_from = WalletTransferForm()

    def build_page():
        pay_logs = UserBalanceLog.query.filter(
            UserBalanceLog.user_id == g.user.id).order_by(UserBalanceLog.id.desc()).limit(50)
        return render_template('application/profile/wallet.html',
                               transfer_from=transfer_from, replenish_from=replenish_from,
                               pay_logs=pay_logs)

    if replenish_from.validate_on_submit():
        amount = float(replenish_from.amount.data)

        pay = Payment.create_pay(amount, "ENOTIO",
                                 payment_system_data={
                                     "comment": f"Пополнение баланса на {amount} руб. для {g.user.bukkit.nickname}"},
                                 useful_data={
                                     "user_uuid": g.user.uuid,
                                     "wallet_amount": amount
                                 })
        return redirect(pay.link)

    if transfer_from.validate_on_submit():
        replenish_from = WalletReplenishForm()

        to_nickname = transfer_from.to_nickname.data
        amount = transfer_from.to_amount.data
        user_balance = g.user.money

        if amount < 0:
            flash("Сумма не может быть меньше 0", FlashTypes.ERROR)
            return build_page()

        if amount == 0:
            flash(f"Сумма должна быть больше {amount} руб.", FlashTypes.ERROR)
            return build_page()

        if amount > user_balance:
            flash(f"У вас недостаточно средств для перевода,"
                  f" пожалуйста пополните баланс на {amount - user_balance} руб", FlashTypes.ERROR)
            return build_page()

        try:
            to_user = User.get_from_nickname(to_nickname)
        except ValueError:
            flash(f"Игрок под никнеймом {to_nickname} никогда не играл на проекте!", FlashTypes.ERROR)
            return build_page()

        if g.user == to_user:
            flash("Вы не можете выполнить перевод самому себе", FlashTypes.ERROR)
            return build_page()

        UserBalanceLog.user_money_edit(g.user, amount * -1, comment=f"Перевод пользователю {to_nickname}")
        UserBalanceLog.user_money_edit(to_user, amount, comment=f"Перевод от пользователя {g.user.bukkit.nickname}")
        flash(f"Вы успешно перевели {amount} руб. Теперь ваш баланс составляет {g.user.money} руб.", FlashTypes.INFO)

    return build_page()


@profile.route('/gifts')
@login_required
def gifts():
    from app.blueprints.gift.engine import UserGift
    user_gifts = UserGift.get_all_from_user(g.user)
    return render_template('application/profile/gifts.html', gifts=user_gifts)


@profile.route('/applications')
@login_required
def applications():
    user_applications = []
    user_applications_models = FormAnswer.get_all_user_answers(g.user)
    for model in user_applications_models:
        try:
            user_applications.append((model, FormEngine.get_from_model(model)))
        except RuntimeError:
            continue
    return render_template('application/profile/applications.html', applications=user_applications,
                           forms=FormEngine.all())
