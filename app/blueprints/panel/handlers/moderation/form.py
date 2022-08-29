from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

from app.helper.wysiwyg import WysiwygField


class NewAlertForm(FlaskForm):
    alert_type = SelectField("Тип", choices=[("warning", "Предупреждение"), ("reprimand", "Выговор")],
                             validators=[DataRequired("Поле должно быть заполнено")])

    reason = WysiwygField("Причина")

    submit = SubmitField('Выдать', render_kw={"class": "btn btn-info btn-block"})
    cancel = SubmitField('Отмена', render_kw={"class": "btn btn-warning btn-block"})


class AlertControlForm(FlaskForm):
    activate = SubmitField('Активировать', render_kw={"class": "btn  btn-round btn-success"})
    deactivate = SubmitField('Аннулировать', render_kw={"class": "btn  btn-round btn-warning"})
    to_moder = SubmitField("К модератору",  render_kw={"class": "btn  btn-round btn-primary"})
