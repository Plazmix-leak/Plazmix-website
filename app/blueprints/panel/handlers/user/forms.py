from flask import request
from flask_wtf import FlaskForm

from wtforms import StringField, RadioField, IntegerField

from wtforms import SubmitField
from wtforms.validators import DataRequired

from app.core.user import User
from app.helper.badges import BadgeCollections


class UserControlForm(FlaskForm):
    password_change = SubmitField('Сменить пароль', render_kw={"class": "btn btn-block btn-info"})
    edit_money = SubmitField('Изменить баланс', render_kw={"class": "btn btn-block btn-warning"})
    badges = SubmitField('Бейджики', render_kw={"class": "btn btn-block btn-primary"})


class UserBannedForm(FlaskForm):
    reason = StringField("Причина блокировки, можно оставить пустым",
                         description="Причина блокировки, можно оставить пустым",
                         render_kw={"class": "form-control border-input",
                                    "placeholder": "Причина блокировки, можно оставить пустым"})
    submit = SubmitField('Выдать', render_kw={"class": "btn btn-block btn-primary"})


class UserMoneyChange(FlaskForm):
    amount = IntegerField("Сумма изменения, для снятия укажите сумму меньше нуля",
                          validators=[DataRequired("Поле должно быть заполнено")],
                          render_kw={"class": "form-control border-input",
                                     "placeholder": "Сумма изменения, для снятия укажите сумму меньше нуля"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-block btn-primary"})


class UserUnBannedForm(FlaskForm):
    submit = SubmitField('Разбанить', render_kw={"class": "btn btn-block btn-primary"})


class UserChangePassword(FlaskForm):
    new_password_one = StringField("", validators=[DataRequired("Поле должно быть заполнено")],
                                   description="Новый пароль",
                                   render_kw={"class": "form-control border-input", "placeholder": "Новый пароль"})

    new_password_two = StringField("", validators=[DataRequired("Поле должно быть заполнено")],
                                   description="Повторите пароль",
                                   render_kw={"class": "form-control border-input",
                                              "placeholder": "Повторите пароль"})

    submit_password = SubmitField('Сохранить', render_kw={"class": "btn btn-info"})


class UserBadgesForm(FlaskForm):
    legend = RadioField("Легендарный игрок", choices=[('yes', "Активен"), ('no', "Не активен")],
                        validators=[DataRequired("Поле должно быть заполнено")],
                        render_kw={"class": "checkbox-radios"})

    verification = RadioField("Верификация", choices=[('yes', "Активен"), ('no', "Не активен")],
                              validators=[DataRequired("Поле должно быть заполнено")],
                              render_kw={"class": "checkbox-radios"})

    partner = RadioField("Партнёр проекта", choices=[('yes', "Активен"), ('no', "Не активен")],
                         validators=[DataRequired("Поле должно быть заполнено")],
                         render_kw={"class": "checkbox-radios"})

    partner_developer = RadioField("Разработчик партнёрского софта", choices=[('yes', "Активен"), ('no', "Не активен")],
                                   validators=[DataRequired("Поле должно быть заполнено")],
                                   render_kw={"class": "checkbox-radios"})

    top_worker = RadioField("Почетный участник команды проекта", choices=[('yes', "Активен"), ('no', "Не активен")],
                            validators=[DataRequired("Поле должно быть заполнено")],
                            render_kw={"class": "checkbox-radios"})

    worker = RadioField("Участник команды проекта", choices=[('yes', "Активен"), ('no', "Не активен")],
                        validators=[DataRequired("Поле должно быть заполнено")],
                        render_kw={"class": "checkbox-radios"})

    plus_sub = RadioField("Подписка +", choices=[('yes', "Активен"), ('no', "Не активен")],
                          validators=[DataRequired("Поле должно быть заполнено")],
                          render_kw={"class": "checkbox-radios"})

    submit = SubmitField('Отправить', render_kw={"class": "btn btn-info"})

    def __init__(self, *args, **kwargs):
        super(UserBadgesForm, self).__init__(*args, **kwargs)
        user: User = kwargs.get('user')
        if request.method.lower() == "post":
            return

        all_badges = BadgeCollections.get_all()
        user_badges = user.badges_list
        for badge in all_badges:
            check = 'no'
            for user_badge in user_badges:
                if badge == user_badge:
                    check = 'yes'
                    break

            getattr(self, badge.technical_name).data = check


class TechnicalSupportPanel(FlaskForm):
    generate_password_reset_link = SubmitField('Восстановление пароля',
                                               render_kw={"class": "btn btn-block btn-success"})


class TSPasswordRequired(FlaskForm):
    generate_password_reset_link = SubmitField('Сгенерировать ссылку',
                                               render_kw={"class": "btn btn-block btn-success"})
    canceled = SubmitField('Отмена',
                           render_kw={"class": "btn btn-block btn-danger"})


class UserSearchForm(FlaskForm):
    nickname_like = StringField("",
                                description="Поисковый запрос",
                                render_kw={"class": "form-control",
                                           "placeholder": "Введите никнейм игрока не менее 3-х символов"})


class ClearGlobalCacheForm(FlaskForm):
    clear = SubmitField('Очистить весь кэш',
                        render_kw={"class": "btn btn-block btn-danger"})


class PermissionEditGroupModeration(FlaskForm):
    junior = SubmitField('Выдать Junior',
                         render_kw={"class": "btn btn-block btn-primary"})
    junior_remove = SubmitField('Снять Junior',
                                render_kw={"class": "btn btn-block btn-danger"})
    moderation = SubmitField('Выдать Moderator',
                             render_kw={"class": "btn btn-block btn-primary"})
    moderation_remove = SubmitField('Снять Moderator',
                                    render_kw={"class": "btn btn-block btn-danger"})
    senior = SubmitField('Выдать Moderator',
                         render_kw={"class": "btn btn-block btn-primary"})
    senior_remove = SubmitField('Снять Moderator',
                                render_kw={"class": "btn btn-block btn-danger"})
    delete_all = SubmitField('Снять с должности модератора',
                             render_kw={"class": "btn btn-block btn-danger"})


class PermissionEditGroupBuilder(FlaskForm):
    build = SubmitField('Выдать BUILDER',
                        render_kw={"class": "btn btn-block btn-primary"})
    remove_build = SubmitField('Снять BUILDER',
                               render_kw={"class": "btn btn-block btn-danger"})
    senior_builder = SubmitField('Выдать Sr. Build',
                                 render_kw={"class": "btn btn-block btn-primary"})
    senior_builder_remove = SubmitField('Снять Sr. Build',
                                        render_kw={"class": "btn btn-block btn-danger"})

    delete_all = SubmitField('Снять с должности билдера',
                             render_kw={"class": "btn btn-block btn-danger"})


class PermissionEditGroupYouTube(FlaskForm):
    add_yt = SubmitField('Выдать YT',
                         render_kw={"class": "btn btn-block btn-primary"})
    remove_yt = SubmitField('Снять YT',
                            render_kw={"class": "btn btn-block btn-danger"})
    add_yt_plus = SubmitField('Выдать YT+',
                              render_kw={"class": "btn btn-block btn-primary"})
    remove_yt_plus = SubmitField('Снять YT+',
                                 render_kw={"class": "btn btn-block btn-danger"})

    delete_all = SubmitField('Снять с должности ютубера',
                             render_kw={"class": "btn btn-block btn-danger"})
