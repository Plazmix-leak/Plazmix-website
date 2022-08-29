import datetime
import os

from flask import render_template
from mailer import Mailer, Message

from app import celery
from app.core.user import User, UserPasswordRestore, EditEmail, UserBalanceLog
from app.lib.ip_position import IpPosition


@celery.task(name="email.user_login")
def email_user_login(user_uuid, ip):
    try:
        user = User.get_from_uuid(uuid=user_uuid)
    except ValueError:
        return "Unknown user"

    if user.email is None:
        return "No email"

    position = IpPosition(ip)
    subject = "Уведомление безопасности"
    text = "Вы получили это письмо, потому что в ваш аккаунт" \
           f" Plazmix {datetime.datetime.now().strftime('%d.%m.%Y в %H:%M')} был выполнен вход, с IP адреса {ip}" \
           f" ({position.get_country}, {position.get_region}, {position.get_city})" \
           f".|Если это были не вы, то срочно смените пароль!"
    html = render_template('email/main.html', target=user, text=text)

    __send(subject=subject, template=html, email=user.email)
    return "Ok"


@celery.task(name="email.user_restore")
def email_user_restore(restore_uuid):
    try:
        restore: UserPasswordRestore = UserPasswordRestore.get_from_uuid(restore_uuid)
    except ValueError:
        return "Unknown restore"

    user = restore.user
    if user.email is None:
        return "No email"

    subject = "Запрос на сброс пароля"
    text = "Вы можете сбросить пароль от Plazmix, перейдя по ссылки ниже." \
           f" Если вы не запрашивали новый пароль, пожалуйста, игнорируйте это письмо.|{restore.link}"
    html = render_template('email/main.html', target=user, text=text)

    __send(subject=subject, template=html, email=user.email)
    return "Ok"


@celery.task(name="email.email_validate")
def email_validate(edit_uuid):
    try:
        edit: EditEmail = EditEmail.get_from_uuid(edit_uuid)
    except ValueError:
        return "Unknown edit"

    user = edit.user

    subject = "Привязка почты к аккаунту"
    text = "Вы можете привязать эту почту к своему аккаунту Plazmix, перейдя по ссылки ниже." \
           f" Если вы не запрашивали новый пароль, пожалуйста, игнорируйте это письмо.|{edit.link}"
    html = render_template('email/main.html', target=user, text=text)
    __send(subject=subject, template=html, email=edit.new_email)
    return "Ok"


@celery.task(name="email.edit_password")
def email_edit_password(user_uuid):
    try:
        user = User.get_from_uuid(uuid=user_uuid)
    except ValueError:
        return "Unknown player"

    if user.email is None:
        return "No email"

    subject = "Ваш пароль изменён"
    text = "Только что на вашем аккаунте был изменён пароль, если это не вы, то срочно сбросьте пароль!|" \
           f"Если вам требуется техническая поддержка, обратитесь к нам - https://plzm.xyz/support"
    html = render_template('email/main.html', target=user, text=text)
    __send(subject=subject, template=html, email=user.email)
    return "Ok"


@celery.task(name="email.wallet")
def email_wallet(log_id):
    try:
        log: UserBalanceLog = UserBalanceLog.get_from_id(log_id)
    except ValueError:
        return "Unknown log"

    user: User = log.user

    if user.email is None:
        return "No email"

    subject = "Plazmix.Wallet изменение вашего баланса"

    text = "Только что, баланс вашего аккаунта был изменён, ниже вы увидите информацию о операции|" \
           f"Дата: {log.datetime.strftime('%d.%m.%Y в %H:%M')}|" \
           f"Описание: {log.comment}|" \
           f"Сумма операции: {log.amount}|" \
           f"Баланс до операции: {log.before_change}|" \
           f"Баланс после операции: {log.after_change}||" \
           f"Если это были не вы, то срочно свяжитесь с поддержкой - https://plzm.xyz/support"
    html = render_template('email/main.html', target=user, text=text)
    __send(subject=subject, template=html, email=user.email)
    return "Ok"


def __send(email, template, subject, attaches=None):
    message = Message(From=f"Plazmix Network <{os.getenv('MAIL_FROM')}>",
                      To=email,
                      charset="utf-8")

    message.Subject = subject
    message.Html = template

    if attaches is not None:
        for attach in attaches:
            message.attach(attach)
    sender = Mailer(host=os.getenv('MAIL_HOST'), port=os.getenv('MAIL_PORT'),
                    usr=os.getenv('MAIL_FROM'), pwd=os.getenv('MAIL_PASSWORD'),
                    use_ssl=False)
    sender.send(message)
