from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired


class ModeratorForm(FlaskForm):
    first_name = StringField("Имя", validators=[DataRequired("Поле должно быть заполнено")],
                             render_kw={"class": "form-control no-border", "placeholder": "Ваше имя"})

    last_name = StringField("Фамилия", validators=[DataRequired("Поле должно быть заполнено")],
                            render_kw={"class": "form-control no-border", "placeholder": "Ваша Фамилия"})

    years = IntegerField("Возраст", validators=[DataRequired("Поле должно быть числом")],
                         render_kw={"class": "form-control no-border", "placeholder": "Возраст"})

    vk = StringField("Ссылка на ваш VK", validators=[DataRequired("Поле должно быть заполнено")],
                     render_kw={"class": "form-control no-border", "placeholder": "Ссылка на ваш VK"})

    timezone = StringField("Часовой пояс", validators=[DataRequired("Поле должно быть заполнено")],
                           render_kw={"class": "form-control no-border", "placeholder": "Ваш часовой пояс"})

    project_time = StringField("Сколько времени вы готовы уделять проекту?",
                               validators=[DataRequired("Поле должно быть заполнено")],
                               render_kw={"class": "form-control no-border",
                                          "placeholder": "Сколько времени вы готовы уделять проекту?"})

    experiences = TextAreaField("Имеется ли у вас опыт в модерировании?",
                                validators=[DataRequired("Поле должно быть заполнено")],
                                render_kw={"class": "form-control no-border",
                                           "placeholder": "Имеется ли у вас опыт в модерировании?"})

    motivation = TextAreaField("Почему вы хотите занять должность модератора?",
                               validators=[DataRequired("Поле должно быть заполнено")],
                               render_kw={"class": "form-control no-border",
                                          "placeholder": "Почему вы хотите занять должность Модератора?"})

    about_us = TextAreaField("Напишите о себе", validators=[DataRequired("Поле должно быть заполнено")],
                             render_kw={"class": "form-control no-border",
                                        "placeholder": "Напишите о себе"})

    microphone = SelectField("Есть ли у вас микрофон",
                             choices=[("Есть", "Есть"), ("Нету", "Нету")])

    interview = SelectField("Готовы ли вы пройти собеседование и проверку ПК",
                            choices=[("Да", "Да"), ("Нет", "Нет")])

    submit = SubmitField('Отправить', render_kw={"class": "btn btn-block btn-round btn-info"})
