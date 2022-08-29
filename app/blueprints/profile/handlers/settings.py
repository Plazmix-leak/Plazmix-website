from flask import g, render_template, redirect, url_for, flash

from app.core.user import User, EditEmail
from app.core.user.module import ExtServicesCode, UserExternalService
from app.helper.decorators.web import login_required
from app.helper.flash_types import FlashTypes
from app.helper.simple_page import SimplePage, PageButton, ButtonType, ErrorPage
from app.helper.tools import get_next_page
from .. import profile
from ..forms import EditEmailForm, EditPasswordForm


@profile.route('/checker')
@login_required
def checker():
    user: User = g.user
    if user.email is None:
        return SimplePage(title="Security",
                          comment="Мы заметили, что к вашему аккаунту не привязана почта,"
                                  " рекомендуем исправить это, для увелечения степени защиты вашего аккаунта",
                          icon="fad fa-shield fa-7x", icon_color="#0b7f94", page_title="Security").add_button(
            PageButton(url=url_for('profile.settings'),
                       text="Перейти в настройки", button_type=ButtonType.COLOR_SUCCESS)).add_button(
            PageButton(url=url_for('main.index'), text="Позже", button_type=ButtonType.LINK_PRIMARY)
        ).build()
    return redirect(get_next_page())


@profile.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    email_form = EditEmailForm()
    password_form = EditPasswordForm()

    def __get_account_or_none(account_code):
        try:
            account = UserExternalService.get_user_service(g.user, account_code)
        except RuntimeError:
            account = None
        return account

    def build_page():
        accounts = {}
        for service in ExtServicesCode:
            accounts[service] = __get_account_or_none(service)
        return render_template('application/profile/settings.html', password_form=password_form,
                               accounts=accounts, email_form=email_form)

    if email_form.validate_on_submit():
        password_form = EditPasswordForm()
        if g.user.email and email_form.new_email.data.lower() == g.user.email.lower():
            flash("Адресс электронной почты свопадает с текущим", FlashTypes.WARNING)
            return build_page()

        try:
            EditEmail.init_from_user(g.user, email_form.new_email.data)
        except RuntimeError:
            flash("Пользователь с таким Email уже существует!", FlashTypes.ERROR)
            return build_page()

        flash("Запрос успешно создан! Проверьте свою почту", FlashTypes.INFO)
        return build_page()

    if password_form.validate_on_submit():
        email_form = EditEmailForm()
        current_pwd = password_form.current_password.data
        new_pwd_one = password_form.new_password_one.data
        new_pwd_two = password_form.new_password_two.data

        if g.user.chek_password(current_pwd) is False:
            flash("Текущий пароль указан неверно!", FlashTypes.ERROR)
            return build_page()

        if new_pwd_one != new_pwd_two:
            flash("Пароли не совпадают", FlashTypes.ERROR)
            return build_page()

        g.user.edit_password(new_pwd_two)
        flash("Пароль успешно изменён!", FlashTypes.INFO)

    return build_page()


@profile.route('/settings/ext/<int:ext_service_id>/edit', methods=['GET', 'POST'])
@login_required
def ext_service_edit(ext_service_id):
    try:
        service: UserExternalService = UserExternalService.get_from_id(ext_service_id)
    except RuntimeError:
        return ErrorPage().build()
    ext_user = service.user
    if g.user.id != ext_user.id:
        return ErrorPage().build()

    if service.visible is True:
        service.set_unvisible()
    else:
        service.set_visible()
    return redirect(url_for('profile.settings'))


@profile.route('/email/validate/<email_edit_uuid>')
@login_required
def email_edit(email_edit_uuid):
    try:
        edit: EditEmail = EditEmail.get_from_uuid(email_edit_uuid)
    except ValueError:
        return ErrorPage(comment="Ссылка недействительная").add_button(
            PageButton(url=url_for('main.index'), text="Главная", button_type=ButtonType.COLOR_PRIMARY)
        ).build()

    if edit.is_active is False:
        return ErrorPage(comment="Ссылка недействительная").add_button(
            PageButton(url=url_for('main.index'), text="Главная", button_type=ButtonType.COLOR_PRIMARY)
        ).build()

    if edit.user != g.user:
        return ErrorPage(comment="Ссылка недействительная").add_button(
            PageButton(url=url_for('main.index'), text="Главная", button_type=ButtonType.COLOR_PRIMARY)
        ).build()

    edit.used()
    return SimplePage(title="Успешно!", page_title="Смена почты", comment=f"Ваша почта успешно"
                                                                          f" изменена на {edit.new_email}",
                      icon="fad fa-check fa-7x",
                      icon_color="#6acd63").build()
