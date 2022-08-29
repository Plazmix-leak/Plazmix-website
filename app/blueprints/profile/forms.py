from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email


class EditPasswordForm(FlaskForm):
    current_password = PasswordField("", validators=[DataRequired("Поле должно быть заполнено")],
                                     description="Текущий пароль",
                                     render_kw={"class": "form-control border-input", "placeholder": "Текущий пароль"})

    new_password_one = PasswordField("", validators=[DataRequired("Поле должно быть заполнено")],
                                     description="Новый пароль",
                                     render_kw={"class": "form-control border-input", "placeholder": "Новый пароль"})

    new_password_two = PasswordField("", validators=[DataRequired("Поле должно быть заполнено")],
                                     description="Повторите пароль",
                                     render_kw={"class": "form-control border-input",
                                                "placeholder": "Повторите пароль"})

    submit_password = SubmitField('Отправить', render_kw={"class": "btn btn-info"})


class EditEmailForm(FlaskForm):
    new_email = StringField("", validators=[DataRequired("Поле должно быть заполнено"),
                                            Email(message="Введите Email")],
                            description="Почта",
                            render_kw={"class": "form-control border-input", "placeholder": "Введите почту"})

    submit_email = SubmitField('Отправить', render_kw={"class": "btn btn-info"})


class WalletReplenishForm(FlaskForm):
    amount = IntegerField("", validators=[DataRequired("Поле не должно быть пустым")],
                          description="Сумма",
                          render_kw={"class": "form-control border-input", "placeholder": "Введите сумму пополнения"})

    submit_replenish = SubmitField('Пополнить', render_kw={"class": "btn btn-success btn-round btn-block"})


class WalletTransferForm(FlaskForm):
    to_nickname = StringField("", validators=[DataRequired("Поле должно быть заполнено")],
                              description="Ник получателя",
                              render_kw={"class": "form-control", "placeholder": "Ник получателя"})

    to_amount = IntegerField("", validators=[DataRequired("Поле не должно быть пустым")],
                             description="Сумма",
                             render_kw={"class": "form-control border-input", "placeholder": "Сумма перевода"})

    submit_transfer = SubmitField('Перевести', render_kw={"class": "btn btn-info btn-round btn-block"})
