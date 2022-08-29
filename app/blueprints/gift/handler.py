from flask import request, g, redirect, url_for

from . import gift as blueprint
from .engine import GiftNotFound, GiftIsNotActiveError
from .engine.engine import GiftEngine
from .engine.models import Gift, UserGift
from .form import GiftForm, GiftOpenForm
from ...helper.decorators.web import login_required
from ...helper.simple_page import ErrorPage, PageButton, SimplePage, ButtonType


@blueprint.route('/<gift_uuid>', methods=['POST', 'GET'])
@login_required
def get_gift(gift_uuid):
    gift_model = Gift.get_from_uuid(gift_uuid)
    if gift_model is None:
        return ErrorPage(comment="Такого подарка не существует или акция уже закончилась").add_button(
            PageButton(url_for('main.index'), "На главную")).build()

    try:
        gift = GiftEngine.get_from_models(gift_model)
    except GiftNotFound:
        return ErrorPage(comment="Такого подарка не существует или акция уже закончилась").add_button(
            PageButton(url_for('main.index'), "На главную")).build()

    if gift.use_link is False:
        return ErrorPage(comment="Такого подарка не существует или акция уже закончилась").add_button(
            PageButton(url_for('main.index'), "На главную")).build()

    form = GiftForm()
    page = SimplePage(page_title="Подарок", title=gift.name, icon="fad fa-gifts fa-8x", form=form,
                      comment="Вы можете взять этот подарок!")

    if gift.active is False:
        return ErrorPage(comment="Такого подарка не существует или акция уже закончилась").add_button(
            PageButton(url_for('main.index'), "На главную")).build()

    users_gift = UserGift.get_all_from_user(g.user)

    for u_gift in users_gift:
        if u_gift.gift_uuid == gift_model.uuid:
            return ErrorPage(comment="Упс! Вы уже взяли этот подарок, нельзя брать подарок повторно").add_button(
                PageButton(url=url_for('profile.gifts'), text="К моим подаркам", button_type=ButtonType.COLOR_SUCCESS)
            ).add_button(
                PageButton(url_for('main.index'), "На главную", button_type=ButtonType.LINK_PRIMARY)).build()

    if form.validate_on_submit():
        try:
            gift.give(g.user)
            return redirect(url_for("profile.gifts"))
        except GiftIsNotActiveError:
            return ErrorPage(comment="Возникла ошибка при активации подарка, повторите попытку").build()
    return page.build()


@blueprint.route('/open/<int:user_gift_id>', methods=["GET", "POST"])
@login_required
def open_gift(user_gift_id):
    try:
        user_gift: UserGift = UserGift.get_from_id(identification=user_gift_id)
    except ValueError:
        return ErrorPage(comment="Неизвестный подарок :(").build()

    if user_gift.user_id != g.user.id:
        return ErrorPage(comment="Опа, а тут котейка. Не ждал такого? А котики они повсюду. Мяфк",
                         icon="fad fa-cat fa-7x", page_title="НАПАДЕНИЕ КОТИКОВ",
                         title="Мяфк", icon_color="#ba70f5").build()

    if user_gift.open is True:
        return ErrorPage(comment="Ой, похоже, что вы уже открыли этот подарок",
                         icon="fad fa-hand-receiving fa-7x",
                         icon_color="#da60f8").add_button(
            PageButton(url=url_for('profile.gifts'), text="К подаркам", button_type=ButtonType.COLOR_SUCCESS)
        ).build()

    form = GiftOpenForm()
    if form.validate_on_submit():
        gift_impl = GiftEngine.get_from_models(user_gift.gift)
        try:
            gift_impl.activate(g.user)
        except Exception:
            return ErrorPage(comment="Упс! Мы встретились с неожиданной ошибкой"
                                     " когда активировали подарок,"
                                     " повторите попытку позже или обратитесь в подержку!").build()
        user_gift.opened()
        return gift_impl.result_page.add_button(
            PageButton(url=url_for('profile.gifts'), text="К подаркам", button_type=ButtonType.COLOR_PRIMARY)
        ).build()

    return SimplePage(title="Ваш подарок",
                      page_title="Открыть подарок",
                      comment=f"Вы можете открыть подарок : {user_gift.gift.name}",
                      icon="fad fa-hand-holding-box fa-7x",
                      icon_color="#60c4f8",
                      form=form).build()
