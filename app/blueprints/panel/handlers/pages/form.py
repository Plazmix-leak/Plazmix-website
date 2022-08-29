from flask import request
from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, TextField, StringField, SelectField
from wtforms.validators import DataRequired

from app.core.pages.models import Page
from app.helper.wysiwyg import WysiwygField


class PageEditor(FlaskForm):
    publish = RadioField("Почетный участник команды проекта", choices=[('yes', "Опубликована"), ('no', "Скрыта")],
                         validators=[DataRequired("Поле должно быть заполнено")],
                         render_kw={"class": "checkbox-radios"})
    title = TextField("Название страницч", validators=[DataRequired("Поле должно быть заполнено")],
                      render_kw={"class": "form-control"})
    content = WysiwygField()
    submit = SubmitField('Отправить', render_kw={"class": "btn  btn-round btn-success"})

    def __init__(self, *args, **kwargs):
        super(PageEditor, self).__init__(*args, **kwargs)

        if request.method.lower() == 'post':
            return

        page: Page = kwargs.get('page_content', None)
        if page is None:
            return

        self.publish.data = 'yes' if page.public else 'no'
        current_version = page.current_version
        self.title.data = current_version.title
        self.content.data = current_version.content


class PageCreate(FlaskForm):
    uri = StringField("Ссылка на страницу", validators=[DataRequired("Поле должно быть заполнено")],
                      render_kw={"class": "form-control"})
    publish = RadioField("Почетный участник команды проекта", choices=[('yes', "Опубликована"), ('no', "Скрыта")],
                         validators=[DataRequired("Поле должно быть заполнено")],
                         render_kw={"class": "checkbox-radios"})
    title = TextField("Название страницч", validators=[DataRequired("Поле должно быть заполнено")],
                      render_kw={"class": "form-control"})
    content = WysiwygField()
    submit = SubmitField('Отправить', render_kw={"class": "btn  btn-round btn-success"})


class PageRollback(FlaskForm):
    version_ident = SelectField("Выберите версию",
                                validators=[DataRequired("Поле должно быть заполнено")],
                                render_kw={"class": "selectpicker"})
    submit = SubmitField('Откатить', render_kw={"class": "btn btn-block btn-round btn-success"})

    def __init__(self, *args, **kwargs):
        pass
