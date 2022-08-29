from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class AppealForm(FlaskForm):
    cause = TextAreaField("Опишите ситуацию максимально подробно",
                          validators=[DataRequired("Заполните это поле")],
                          render_kw={"class": "form-control no-border",
                                     "placeholder": "Опишите ситуацию максимально подробно"})

    proof = TextAreaField("Доказательства вашей невиновности",
                          validators=[DataRequired("Заполните это поле")],
                          render_kw={"class": "form-control no-border",
                                     "placeholder": "Доказательства вашей невиновности"})

    responsibility = SelectField("Готовы нести ответственность в случае обмана?",
                                 choices=[("Да", "Да"), ("Нет", "Нет")])

    submit = SubmitField('Отправить', render_kw={"class": "btn btn-block btn-round btn-info"})
