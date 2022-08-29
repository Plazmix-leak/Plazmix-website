from authlib.oauth2 import OAuth2Error
from flask import g, url_for, redirect, flash, request, render_template
from string import ascii_letters, digits

from app.core.developers.oauth.ext import authorization
from app.core.user import User, UserAuthSession, UserPasswordRestore
from app.core.user.module import ExtServicesCode
from app.errors import AuthError
from app.helper.decorators.web import login_required
from app.helper.flash_types import FlashTypes
from app.helper.simple_page import SimplePage, ErrorPage, PageButton, ButtonType
from app.helper.template import get_random_background
from . import auth
from .forms import LoginForm, RestoreInitForm, RestorePasswordForm, OauthValidationForm, RegistrationForm
from ...helper.tools import get_next_page


@auth.route("/login", methods=["GET", "POST"])
def login():
    if g.user is not None:
        return redirect(url_for("main.index"))

    form = LoginForm()
    page = SimplePage(page_title="Авторизация", title="Авторизация",
                      icon=None,
                      comment=render_template('application/auth/auth_variants.html', services=ExtServicesCode),
                      form=form).add_button(
        PageButton(url=url_for('auth.restore'), text="Забыли пароль?", button_type=ButtonType.LINK_PRIMARY)
    ).add_button(
        PageButton(url=url_for('auth.registration_profile'),
                   text="Создать аккаунт", button_type=ButtonType.LINK_PRIMARY))

    if form.validate_on_submit():
        try:
            try:
                user: User = User.login(form.login.data, form.password.data)
            except ValueError:
                flash("Игрок с таким никнеймом никогда не играл на проекте", FlashTypes.ERROR)
                return page.build()
            UserAuthSession.new_session(user, "site")
        except AuthError as ae:
            flash(ae.get_reason, FlashTypes.ERROR)
            return page.build()
        return redirect(url_for("profile.checker") + f"?next={get_next_page()}")
    return page.build()


@auth.route("/registration", methods=["GET", "POST"])
def registration_profile():
    if g.user is not None:
        flash("Вы уже зарегистрированы на проекте!", FlashTypes.ERROR)
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    page = SimplePage(page_title="Регистрация", title="Регистрация",
                      icon=None, comment="<p>Создавая аккаунт на сайте, вы создаёте такой-же аккаунт на сервере"
                                         ", поэтому используйте ник с которым вы будете играть!"
                                         " Если у вас уже есть аккаунт на сервере ТО ВОЙДИТЕ под"
                                         " ним на сайт, а не создавайте новый!</p>",
                      form=form).add_button(
        PageButton(url=url_for('auth.login'), text="У меня уже есть аккаунт", button_type=ButtonType.LINK_PRIMARY))

    if form.validate_on_submit():
        if form.password.data != form.password_2.data:
            flash("Пароли не совпадают!", FlashTypes.ERROR)
            return page.build()

        new_nickname = form.nickname.data.replace(" ", "")
        nickname_len = len(new_nickname)
        if nickname_len > 16 or nickname_len < 3:
            flash("Ник должен быть от 3 до 16-ти символов!", FlashTypes.ERROR)
            return page.build()

        valid_symbols = ascii_letters + digits + "_"

        for nickname_element in new_nickname:
            if nickname_element not in valid_symbols:
                flash("Никнейм содержит запрещённые символы, разрешены только цифры и латинские буквы!",
                      FlashTypes.ERROR)
                return page.build()

        try:
            new_user = User.registration(new_nickname, form.password_2.data)
        except AuthError as ae:
            flash(ae.get_reason, FlashTypes.ERROR)
            return page.build()

        UserAuthSession.new_session(new_user, "site")
        flash("Спасибо за регистрацию на проекте!", FlashTypes.INFO)
        return redirect(url_for("profile.checker") + f"?next={get_next_page()}")

    return page.build()


@auth.route("/restore", methods=["GET", "POST"])
def restore():
    if g.user is not None:
        flash("Вы ужа авторизованы!", FlashTypes.ERROR)
        return redirect(url_for("main.index"))

    form = RestoreInitForm()
    page = SimplePage(page_title="Сброс пароля", title="Сброс пароля",
                      icon=None, comment=None, form=form).add_button(
        PageButton(url=url_for("auth.login"), text="Авторизация", button_type=ButtonType.LINK_PRIMARY))

    if form.validate_on_submit():

        try:
            user: User = User.get_from_nickname(nickname=form.login.data)
        except ValueError:
            flash("Игрок с таким никнеймом никогда не играл на проекте", FlashTypes.ERROR)
            return page.build()

        if user.email is None:
            return ErrorPage(comment="У данного игрока не привязан Email адрес,"
                                     " автоматический сброс пароля невозможен."
                                     " Свяжитесь с технической поддержкой").build()

        UserPasswordRestore.init_from_user(user)
        return SimplePage(title="Запрос отправлен",
                          comment="Запрос на сброс пароля успешно отправлен. Проверьте почту",
                          page_title="Запрос отправлен",
                          icon="fad fa-check fa-7x",
                          icon_color="#38940b").build()

    else:
        return page.build()


@auth.route('/restore/<restore_uuid>', methods=["GET", "POST"])
def restore_password(restore_uuid):
    if g.user is not None:
        flash("Вы ужа авторизованы!", FlashTypes.ERROR)
        return redirect(url_for("main.index"))

    try:
        pwd_restore: UserPasswordRestore = UserPasswordRestore.get_from_uuid(restore_uuid)
    except ValueError:
        return ErrorPage(comment="Ссылка недействительная").build()

    if pwd_restore.is_active is False:
        return ErrorPage(comment="Ссылка недействительная").build()

    form = RestorePasswordForm()
    page = SimplePage(title="Сброс пароля", comment=None, page_title="Сброс пароля", form=form, icon=None)

    if form.validate_on_submit():
        new_pwd_one = form.password_one.data
        new_pwd_two = form.password_two.data
        if new_pwd_one != new_pwd_two:
            flash("Пароли не совподают", FlashTypes.ERROR)
            return page.build()
        try:
            pwd_restore.used(new_pwd_two)
        except RuntimeError:
            return ErrorPage(comment="Возникла непредвиденная ошибка при смене пароля,"
                                     " пожалуйста обратитесь в техническую поддержку проекта").build()

        return SimplePage(title="Успешно", page_title="Сброс пароля",
                          comment="Пароль успешно изменён, теперь вы можете зайти на сайт или сервер!",
                          icon="fad fa-check-double fa-7x",
                          icon_color="#38940b").add_button(
            PageButton(url=url_for('auth.login'), text="Авторизация")).build()

    else:
        return page.build()


@auth.route('/oauth2/authorize', methods=['GET', 'POST'])
@login_required
def login_oauth_authorize():
    user = g.user
    form = OauthValidationForm()

    if request.method.lower() == 'get':
        try:
            grant = authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            return ErrorPage(comment=error.error).build()
        return render_template('application/auth/oauth.html', user=user,
                               grant=grant, background=get_random_background(),
                               app=grant.client, form=form)

    if form.validate_on_submit():
        if form.success.data:
            return authorization.create_authorization_response(grant_user=user)
    flash("Авторизация отменена или произошла ошибка", FlashTypes.WARNING)
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    session: UserAuthSession = g.session
    session.kill()
    return redirect(url_for("main.index"))
