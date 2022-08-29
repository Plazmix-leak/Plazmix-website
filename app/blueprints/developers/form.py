from flask_wtf import FlaskForm, RecaptchaField

from wtforms import SubmitField, StringField, PasswordField
from flask_wtf.recaptcha.validators import Recaptcha as RecaptchaValidator
from wtforms.validators import DataRequired

from app import app


class CreateDevelopmentTeamForm(FlaskForm):
    name = StringField("Название команды", validators=[DataRequired("Поле должно быть заполнено")],
                       render_kw={"class": "form-control no-border", "placeholder": "Название команды"})

    if app.config.get('DEVELOPMENT', False) is False:
        captcha = RecaptchaField("Проверка на робота", validators=[RecaptchaValidator("Проверка не пройдена")])
    submit = SubmitField('Создать', render_kw={"class": "btn btn-block btn-round btn-info"})


class CreateApiApplication(FlaskForm):
    name = StringField("Название приложения", validators=[DataRequired("Поле должно быть заполнено")],
                       render_kw={"class": "form-control no-border", "placeholder": "Название команды"})
    if app.config.get('DEVELOPMENT', False) is False:
        captcha = RecaptchaField("Проверка на робота", validators=[RecaptchaValidator("Проверка не пройдена")])
    create = SubmitField('Создать', render_kw={"class": "btn btn-block btn-info"})


class CreateOauthApplication(FlaskForm):
    # client_uri = StringField("Client URI", validators=[DataRequired("Поле должно быть заполнено")],
    #                          render_kw={"class": "form-control no-border", "placeholder": "Client URI"})
    name = StringField("Название приложения", validators=[DataRequired("Поле должно быть заполнено")],
                       render_kw={"class": "form-control no-border", "placeholder": "Название команды"})
    redirect_url = StringField("URL редиректа", validators=[DataRequired("Поле должно быть заполнено")],
                               render_kw={"class": "form-control no-border", "placeholder": "Redirect URI"})

    if app.config.get('DEVELOPMENT', False) is False:
        captcha = RecaptchaField("Проверка на робота", validators=[RecaptchaValidator("Проверка не пройдена")])
    submit = SubmitField('Создать', render_kw={"class": "btn btn-block btn-info"})
