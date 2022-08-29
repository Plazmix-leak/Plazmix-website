from json import JSONDecodeError

from authlib.integrations.base_client import OAuthError
from authlib.oauth2.rfc6749 import OAuth2Token
from flask import g, redirect, url_for, flash

from app import oauth_client
from app.core.user import UserAuthSession
from app.core.user.module import ExtServicesCode, UserExternalService
from app.helper.flash_types import FlashTypes
from app.helper.simple_page import ErrorPage, PageButton
from .. import profile


@profile.route('/external/authorize/<service_name>')
def ext_authorize_service(service_name):
    try:
        service_code = ExtServicesCode(service_name)
    except ValueError:
        return ErrorPage(comment="Данный сервис не поддерживается!").build()

    service_instance = getattr(oauth_client, service_code.value, None)
    if service_instance is None:
        return ErrorPage(comment="Инстанция не найдена, свяжитесь с тех. поддержкой!").build()

    return service_instance.authorize_redirect(url_for(f'profile.ext_connect_service', service_name=service_code.value,
                                                       _external=True))


@profile.route('/external/connection/<service_name>')
def ext_connect_service(service_name):
    try:
        service_code = ExtServicesCode(service_name)
    except ValueError:
        return ErrorPage(comment="Данный сервис не поддерживается!").build()

    service_instance = getattr(oauth_client, service_code.value, None)
    if service_instance is None:
        return ErrorPage(comment="Инстанция не найдена, свяжитесь с тех. поддержкой!").build()
    token: OAuth2Token = service_instance.authorize_access_token(
        method='GET' if service_code == ExtServicesCode.VK else 'POST')

    if service_code == ExtServicesCode.DISCORD:
        resp = oauth_client.discord.get('users/@me', token=token)
        try:
            resp_data = resp.json()
        except JSONDecodeError:
            return ErrorPage(comment="Ошибка при обработке запроса, свяжитесь с тех. поддержкой!").build()

        user_name_service = f"{resp_data.get('username')}#{resp_data.get('discriminator')}"
        account_id = resp_data['id']
    elif service_code == ExtServicesCode.VK:
        account_id = dict(token).get('user_id')
        resp = service_instance.get('users.get', params={"v": "5.131",
                                                         "user_ids": str(account_id)},
                                    token=token)
        try:
            resp_data = resp.json().get('response', [{}])[0]
        except JSONDecodeError:
            return ErrorPage(comment="Ошибка при обработке запроса, свяжитесь с тех. поддержкой!").build()

        user_name_service = f"{resp_data.get('first_name', 'ОШИБКА')} {resp_data.get('last_name', 'ОШИБКА')}"

    else:
        return ErrorPage(comment="Слушатель не найден, свяжитесь с тех. поддержкой!")

    if g.user is None:
        try:
            find_account: UserExternalService = UserExternalService.get_from_service_account_id(
                service_code=service_code,
                account_id=account_id)
            user = find_account.user
            UserAuthSession.new_session(user, "site")
            return redirect(url_for('main.index'))
        except RuntimeError:
            flash(f"Аккаунт {service_code.value} не найден", FlashTypes.ERROR)
            return redirect(url_for('auth.login'))

    try:
        ext_service: UserExternalService = UserExternalService.get_from_service_account_id(service_code, account_id)
        if ext_service.user_id != g.user.id:
            return ErrorPage(comment=f"Данный аккаунт {service_code.value} уже"
                                     f" привязан к другому пользователю!").build()
    except RuntimeError:
        pass

    UserExternalService.create_new_or_replace(user=g.user,
                                              service_code=service_code,
                                              user_id_service=account_id,
                                              service_metadata=resp_data,
                                              user_nickname_service=user_name_service)
    flash(f"Аккаунт {service_code.value} {user_name_service} успешно привязан к PlazmixNetwork!", FlashTypes.INFO)
    return redirect(url_for('profile.settings'))


@profile.errorhandler(OAuthError)
def handle_error(error):
    return ErrorPage(title="Oauth2 ошибка", comment=str(error)).add_button(
        PageButton(url="https://vk.me/plazmixnetwork", text="Связаться с тех поддержкой")).build()
