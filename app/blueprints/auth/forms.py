from app import app
from flask_wtf import FlaskForm
from flask_wtf.recaptcha.validators import Recaptcha as RecaptchaValidator

from flask_wtf import RecaptchaField

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired("Поле должно быть заполнено")],
                        description="Ник в игре или почта",
                        render_kw={"class": "form-control no-border", "placeholder": "Ник в игре или почта"})
    password = PasswordField("Пароль", validators=[DataRequired("Поле должно быть заполнено")],
                             description="Пароль",
                             render_kw={"class": "form-control no-border", "placeholder": "Пароль"})
    if app.config.get('DEVELOPMENT', False) is False:
        captcha = RecaptchaField("Проверка на робота", validators=[RecaptchaValidator("Проверка не пройдена")])
    submit = SubmitField('Войти', render_kw={"class": "btn btn-block btn-round btn-info"})


class RegistrationForm(FlaskForm):
    nickname = StringField("Логин", validators=[DataRequired("Поле должно быть заполнено")],
                           description="Ник в игре",
                           render_kw={"class": "form-control no-border", "placeholder": "Ник в игре"})

    password = PasswordField("Пароль", validators=[DataRequired("Поле должно быть заполнено")],
                             description="Пароль",
                             render_kw={"class": "form-control no-border", "placeholder": "Пароль"})

    password_2 = PasswordField("Пароль", validators=[DataRequired("Поле должно быть заполнено")],
                               description="Пароль",
                               render_kw={"class": "form-control no-border", "placeholder": "Пароль"})

    if app.config.get('DEVELOPMENT', False) is False:
        captcha = RecaptchaField("Проверка на робота", validators=[RecaptchaValidator("Проверка не пройдена")])

    submit = SubmitField('Создать', render_kw={"class": "btn btn-block btn-round btn-info"})


class RestoreInitForm(FlaskForm):
    login = StringField("Никнейм", validators=[DataRequired("Поле должно быть заполнено")],
                        description="Ник в игре",
                        render_kw={"class": "form-control no-border", "placeholder": "Ник в игре"})
    if app.config.get('DEVELOPMENT', False) is False:
        captcha = RecaptchaField("Проверка на робота", validators=[RecaptchaValidator("Проверка не пройдена")])
    submit = SubmitField('Отправить запрос', render_kw={"class": "btn btn-block btn-round btn-info"})


class RestorePasswordForm(FlaskForm):
    password_one = PasswordField("Введите новый пароль", validators=[DataRequired("Поле должно быть заполнено")],
                                 description="Введите новый пароль",
                                 render_kw={"class": "form-control no-border", "placeholder": "Введите новый пароль"})
    password_two = PasswordField("Повторите пароль", validators=[DataRequired("Поле должно быть заполнено")],
                                 description="Повторите пароль",
                                 render_kw={"class": "form-control no-border", "placeholder": "Повторите пароль"})
    if app.config.get('DEVELOPMENT', False) is False:
        captcha = RecaptchaField("Проверка на робота", validators=[RecaptchaValidator("Проверка не пройдена")])
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-block btn-round btn-info"})


class OauthValidationForm(FlaskForm):
    success = SubmitField('Авторизоваться', render_kw={"class": "btn btn-block btn-info"})
    canceled = SubmitField('Отмена', render_kw={"class": "btn btn-outline-warning btn-block"})
