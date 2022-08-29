from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class YouTubeForm(FlaskForm):
    channel_link = StringField("Ссылка на ваш канал", validators=[DataRequired("Поле должно быть заполнено")],
                               render_kw={"class": "form-control no-border", "placeholder": "Ссылка на ваш канал"})

    average_views = IntegerField("Сколько у вас в среднем просмотров на видео?",
                                 validators=[DataRequired("Поле должно быть числом")],
                                 render_kw={"class": "form-control no-border",
                                            "placeholder": "Сколько у вас в среднем просмотров на видео?"})

    screen_shot = StringField("Сделайте скриншот своего канала и загрузите на любой фото-хостинг",
                              validators=[DataRequired("Поле должно быть заполнено")],
                              render_kw={"class": "form-control no-border",
                                         "placeholder":
                                             "Сделайте скриншот своего канала и загрузите на любой фото-хостинг"})

    video_release = StringField("Как часто вы собираетесь выпускать видео на сервере?",
                                validators=[DataRequired("Как часто вы собираетесь выпускать видео на сервере?")],
                                render_kw={"class": "form-control no-border",
                                           "placeholder": "Как часто вы собираетесь выпускать видео на сервере?"})

    submit = SubmitField('Отправить', render_kw={"class": "btn btn-block btn-round btn-info"})
