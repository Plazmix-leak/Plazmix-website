from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class UserReportForm(FlaskForm):
    intruder_nickname = StringField("Никнейм нарушителя", validators=[DataRequired("Поле должно быть заполнено")],
                                    render_kw={"class": "form-control no-border", "placeholder": "Никнейм нарушителя"})

    proof = TextAreaField("Доказательства (загрузите на любой фото/видео хостинг)",
                          validators=[DataRequired("Поле должно быть заполнено")],
                          render_kw={"class": "form-control no-border",
                                     "placeholder": "Доказательства (загрузите на любой фото/видео хостинг)"})

    reason = TextAreaField("Суть жалобы (опишите нарушение максимально подробно)",
                           validators=[DataRequired("Поле должно быть заполнено")],
                           render_kw={"class": "form-control no-border",
                                      "placeholder": "Суть жалобы (опишите нарушение максимально подробно)"})

    submit = SubmitField('Отправить', render_kw={"class": "btn btn-block btn-round btn-info"})
