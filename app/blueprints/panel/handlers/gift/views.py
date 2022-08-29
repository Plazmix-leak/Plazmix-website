import uuid

from flask import render_template, abort, url_for, redirect

from app.helper.simple_page import PageButton, ButtonType
from app.blueprints.gift.engine.models import Gift
from app.blueprints.gift.engine.specail_author import SpecialAuthor
from app.core.permissions import Permissions, rule_access_check
from app.helper.simple_page.panel import AdminPanelErrorPage, AdminPanelSimplePage
from ... import panel
from .form import GiftCreateGroupForm, GiftCreateMoneyForm


@panel.route('/gift/list')
@rule_access_check(Permissions.ADMIN_ACCESS)
def gifts_list():
    gifts = Gift.get_from_special_author(SpecialAuthor.PLAZMIX)
    return render_template('adminpanel/elements/gift/list.html', gifts=gifts)


@panel.route('/gift/link/<gift_uid>')
@rule_access_check(Permissions.ADMIN_ACCESS)
def view_gift_link(gift_uid):
    gift = Gift.get_from_uuid(gift_uid)
    if gift is None:
        return abort(404)
    return AdminPanelSimplePage(title="Ссылка на подарок",
                                comment=f"Ссылка на подарок - {url_for('gift.get_gift', gift_uuid=gift.uuid)}"
                                ).add_button(PageButton(url_for("panel.gifts_list"),
                                                        text="К списку подарков",
                                                        button_type=ButtonType.COLOR_SUCCESS)).build()


@panel.route('/gift/create/<gift_type>/<gift_uri>', methods=['GET', 'POST'])
@rule_access_check(Permissions.ADMIN_ACCESS)
def gift_edit(gift_type, gift_uri):
    error_unknown = AdminPanelErrorPage(
        comment="Неизвестный тип подарка или подарок не найден!")

    gift = Gift.get_from_uuid(gift_uri)
    if gift is None:
        return error_unknown.build()

    if gift_type == "money":
        form = GiftCreateMoneyForm.generate_from_gift(gift)
    elif gift_type == "group":
        form = GiftCreateGroupForm.generate_from_gift(gift)
    else:
        return error_unknown.build()

    page = AdminPanelSimplePage(title="Создание подарка",
                                comment=f"Вы изменяете подарок типа {gift_type.lower()}| {gift.name}",
                                form=form)

    if form.validate_on_submit():
        if gift_type == "money":
            meta_data = {"amount": form.amount.data}
        elif gift_type == "group":
            meta_data = {"group": form.group.data}
        else:
            return error_unknown.build()

        gift.update(
            uuid=form.uri.data,
            name=form.name.data,
            link_usage_limit=form.limit.data,
            technical_name=gift_type.lower(),
            data=meta_data,
            author_uuid=SpecialAuthor.PLAZMIX.value,
            use_link=True,
            active=form.active.data or False
        )

        return redirect(url_for("panel.view_gift_link", gift_uid=gift.uuid))

    return page.build()


@panel.route('/gift/create/<gift_type>', methods=['GET', 'POST'])
@rule_access_check(Permissions.ADMIN_ACCESS)
def gift_create(gift_type):
    error_unknown = AdminPanelErrorPage(
        comment="Неизвестный тип подарка!")
    if gift_type == "money":
        form = GiftCreateMoneyForm()
    elif gift_type == "group":
        form = GiftCreateGroupForm()
    else:
        return error_unknown.build()

    page = AdminPanelSimplePage(title="Создание подарка", comment=f"Вы создаете подарок типа {gift_type.lower()}",
                                form=form)

    if form.validate_on_submit():
        if gift_type == "money":
            meta_data = {"amount": form.amount.data}
        elif gift_type == "group":
            meta_data = {"group": form.group.data}
        else:
            return error_unknown.build()

        gift_uid = form.uri.data
        if not gift_uid:
            gift_uid = uuid.uuid4().hex

        gift = Gift.create(uuid=gift_uid,
                           name=form.name.data,
                           link_usage_limit=form.limit.data,
                           technical_name=gift_type.lower(),
                           data=meta_data,
                           author_uuid=SpecialAuthor.PLAZMIX.value,
                           use_link=True,
                           active=form.active.data or False)
        return redirect(url_for("panel.view_gift_link", gift_uid=gift.uuid))

    return page.build()
