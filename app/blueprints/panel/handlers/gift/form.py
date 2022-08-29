from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, RadioField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class GiftCreateGroupForm(FlaskForm):
    name = StringField("Название подарка", validators=[DataRequired("Поле должно быть заполнено")],
                       render_kw={"class": "form-control"})

    uri = StringField("Ссылка на подарок (не обязательное)",
                      render_kw={"class": "form-control"})

    active = BooleanField("Активно", validators=[DataRequired("Поле должно быть заполнено")],
                          render_kw={"class": "form-control border-input",
                                     "placeholder": "Повторите пароль"})

    group = RadioField("Доант группа",
                       choices=[('STAR', "STAR"),
                                ('COSMO', "COSMO"),
                                ('GALAXY', "GALAXY"),
                                ('UNIVERSE', "UNIVERSE"),
                                ('LUXURY', "LUXURY")],
                       validators=[DataRequired("Поле должно быть заполнено")],
                       render_kw={"class": "checkbox-radios"})

    limit = IntegerField("Лимит по использованию",
                         render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn  btn-round btn-success"})

    @classmethod
    def generate_from_gift(cls, gift):
        i = cls()
        if request.method.lower() == "get":
            i.name.data = gift.name
            i.uri.data = gift.uuid
            i.active.data = gift.active
            i.group.data = gift.data.get('group', 'STAR')
            i.limit.data = gift.link_usage_limit
        return i


class GiftCreateMoneyForm(FlaskForm):
    name = StringField("Название подарка", validators=[DataRequired("Поле должно быть заполнено")],
                       render_kw={"class": "form-control"})

    uri = StringField("Ссылка на подарок (не обязательное)",
                      render_kw={"class": "form-control"})

    active = BooleanField("Активно", validators=[DataRequired("Поле должно быть заполнено")],
                          render_kw={"class": "form-control border-input",
                                     "placeholder": "Повторите пароль"})

    amount = IntegerField("Колличество монет", validators=[DataRequired("Поле должно быть заполнено")],
                          render_kw={"class": "form-control"})

    limit = IntegerField("Лимит по использованию",
                         render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn  btn-round btn-success"})

    @classmethod
    def generate_from_gift(cls, gift):
        i = cls()
        if request.method.lower() == "get":
            i.name.data = gift.name
            i.uri.data = gift.uuid
            i.active.data = gift.active
            i.amount.data = gift.data.get('amount', 0)
            i.limit.data = gift.link_usage_limit
        return i
