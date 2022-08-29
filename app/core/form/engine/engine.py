from typing import List

from .base import FormBase
from ..forms.appeal import AppealForm, AppealFormDataClass
from ..forms.moderator import ModeratorForm, ModeratorFormDataClass, ModerFormAdmin
from ..forms.youtube import YouTubeForm, YouTubeFormDataClass, YTFormAdmin
from ..forms.builder import BuilderForm, BuilderFormDataClass, BuilderFormAdmin
from ..forms.report import UserReportForm, UserReportFormDataClass
from ..models.answer import FormAnswer
from ..validator import ThirtyDaysValidation, HourValidation, \
    ActiveAccountValidator, VKAccountValidator, DeactivateValidation


class FormEngine:
    FORMS = [
        FormBase("moderation", "Заявка на модератора",
                 "<center><strong>Вы можете подать заявку если ваш возраст превышает 16 лет</strong></center>",
                 ModeratorForm, ModeratorFormDataClass, [ThirtyDaysValidation(),
                                                         ActiveAccountValidator(), VKAccountValidator()],
                 ModerFormAdmin),

        FormBase("youtube", "Заявка на медиа статус",
                 "<center><strong>Главным критерием для статуса ютубера является активность на Вашем канале."
                 " Если у Вас нет необходимого кол-во подписчиков, но активность соответствует "
                 "требованиям, то администрация может сделать для Вас исключение.</strong>"
                 "<h5>Минимальные требования на статус:</h5>"
                 "<p>- Иметь на своем ютуб канале более 3000 подписчиков.</p>"
                 "<p>- Иметь более 2-х видеороликов на нашем сервере. </p>"
                 "<p>- Иметь активную аудиторию в размере 500 просмотров на каждом ролике.</p>"
                 "<p>- Снимать видеоролики раз в неделю. </p>"
                 "<p>- Активно выкладывать видеоролики на нашем сервере от 1-го видео в месяц.</p></center>",
                 YouTubeForm, YouTubeFormDataClass, [ThirtyDaysValidation(), ActiveAccountValidator(),
                                                     VKAccountValidator()],
                 YTFormAdmin),

        FormBase("builder", "Заявка на билдера", "<strong>Минимальные условия для получения статуса:</strong>"
                                                 " <p>Обязательное соблюдение ВСЕХ правил проекта.</p>"
                                                 " <p>Быть стрессоустойчивым и бесконфликтным человеком. </p>"
                                                 "<p>Быть готовым выслушивать критику и рекомендации.</p>"
                                                 "<p> Уметь пользоваться плагинами по типу WorldEdit, GoBrush.</p>"
                                                 "<p>Наличие свободного времени.</p>"
                                                 "<p>Иметь при себе портфолио своих работ.</p>"
                                                 "<p>Скриншоты ваших работ должны быть сделаны"
                                                 " без ресурспаков и шейдеров.</p><br><p>Удачи!</p>",
                 BuilderForm, BuilderFormDataClass, [ThirtyDaysValidation(), ActiveAccountValidator()],
                 BuilderFormAdmin),

        FormBase("appeal", "Апелляция",
                 "<p>Будьте адекватным при подаче апелляции. Терпеливо ждите рассмотрения апелляции."
                 f" Загружайте доказательства на такие фотохостинги как:</p> <p><a href='https://imgur.com'"
                 f" style='color: #007bff;'>"
                 f"www.imgur.com</a></p> <p><a href='https://yapx.com' style='color: #007bff;'>"
                 f"www.yapx.com</a></p> <p>Старайтесь "
                 "описывать суть максимально понятно и без лишней воды.</p>",
                 AppealForm, AppealFormDataClass, [ThirtyDaysValidation(), DeactivateValidation()],
                 ModerFormAdmin),

        FormBase("report", "Жалоба на игрока", "Не подавайте жалобы на одно и тоже нарушение от одного игрока"
                                               " несколько раз. Ваша жалоба не будет рассмотрена,"
                                               " если истек срок нарушения (7 дней)."
                                               " Запись нарушения должна быть в минимум 480p и 20 фпс. "
                                               "Если Вы находитесь в ЧС сервера, то Ваша жалоба может быть отклонена.",
                 UserReportForm, UserReportFormDataClass, [HourValidation(), DeactivateValidation()],
                 ModerFormAdmin)
    ]

    @classmethod
    def get_from_technical_name(cls, technical_name: str) -> FormBase:
        for page in cls.FORMS:
            if page.technical_name == technical_name:
                return page
        raise ValueError("Unknown form")

    @classmethod
    def get_from_answer_id(cls, answer_id) -> FormBase:
        try:
            answer: FormAnswer = FormAnswer.get_from_id(answer_id)
        except ValueError:
            raise RuntimeError("Unknown answer")

        try:
            base = cls.get_from_technical_name(answer.form_technical_name)
        except ValueError:
            raise RuntimeError("Unknown form ")
        return base

    @classmethod
    def get_from_model(cls, model) -> FormBase:
        return cls.get_from_answer_id(model.id)

    @classmethod
    def all(cls) -> List[FormBase]:
        return cls.FORMS
