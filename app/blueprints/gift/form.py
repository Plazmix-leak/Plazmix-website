from flask_wtf import FlaskForm
from flask_wtf import RecaptchaField
from flask_wtf.recaptcha.validators import Recaptcha as RecaptchaValidator
from wtforms import SubmitField

from app import app


class GiftForm(FlaskForm):
    if app.config.get('DEVELOPMENT', False) is False:
        captcha = RecaptchaField("", validators=[RecaptchaValidator("Проверка не пройдена")])
    submit = SubmitField('Взять подарок', render_kw={"class": "btn btn-block btn-info"})


class GiftOpenForm(FlaskForm):
    open = SubmitField("Открыть подарок", render_kw={"class": "btn btn-block btn-success"})
