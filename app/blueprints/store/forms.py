from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, FloatField
from wtforms.validators import DataRequired


class PaymentType(FlaskForm):
    payment = SelectField("", choices=[("wallet", "Баланс аккаунта"), ("ENOTIO", "Enot.io")],
                          validators=[DataRequired("Поле должно быть заполнено")],
                          render_kw={"class": "selectpicker"})

    submit = SubmitField('Далее', render_kw={"class": "btn btn-block btn-round btn-info"})


class PaymentGenerateForm(FlaskForm):
    nickname = StringField("Ник", validators=[DataRequired("Поле должно быть заполнено")],
                           render_kw={"class": "form-control no-border", "placeholder": "Ник в игре"})

    amount = FloatField("Сумма", validators=[DataRequired("Поле должно быть заполнено")],
                        render_kw={"class": "form-control no-border", "disabled": True})

    submit = SubmitField('Оплатить', render_kw={"class": "btn btn-block btn-round btn-info"})


class PaymentWallet(FlaskForm):
    submit = SubmitField('Оплатить', render_kw={"class": "btn btn-block btn-round btn-info"})