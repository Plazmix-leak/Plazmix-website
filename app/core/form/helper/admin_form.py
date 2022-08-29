from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField


class AdminEditDefaultStatus(FlaskForm):
    success_button = SubmitField('Принять', render_kw={"class": "btn btn-block btn-success"})
    check_button = SubmitField('Отметить', render_kw={"class": "btn btn-block btn-warning"})
    refusal_button = SubmitField('Отклонить', render_kw={"class": "btn btn-block btn-danger"})


class AdminFailStatusConfirmation(FlaskForm):
    fail_comment = TextField("",
                             render_kw={"class": "form-control",
                                        "placeholder": "Прокомментируйте причину отказа"})
    fail_status_submit = SubmitField('Отправить', render_kw={"class": "btn btn-block btn-primary"})
