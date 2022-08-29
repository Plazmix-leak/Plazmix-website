import datetime

import humanize
from flask import request
from pydantic import BaseModel

from app import db
from app.core.form.status import AnswerStatus
from app.core.user import User
from app.lib.ip_position import IpPosition


class FormAnswer(db.Model):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="form_answers", uselist=False)

    form_technical_name = db.Column(db.String(50), nullable=False)
    form_data = db.Column(db.JSON)

    processed_status = db.Column(db.Enum("WAIT", "REFUSAL", "ACCEPTED", "CHECK"))
    processed_comment = db.Column(db.Text)

    ip = db.Column(db.String(50))
    location = db.Column(db.String(200), nullable=True)

    def update_status(self, new_status, status_comment=None):
        self.processed_status = new_status.value
        self.processed_comment = status_comment
        db.session.commit()

    @property
    def status(self):
        return AnswerStatus(self.processed_status)

    @property
    def human_date(self):
        if self.datetime is None:
            return "Неизвестно"

        _t = humanize.i18n.activate("ru_RU")
        return humanize.naturalday(self.datetime)

    @staticmethod
    def can_submit(technical_name: str, user: User, delay=30 * 24 * 3600) -> bool:
        try:
            last: FormAnswer = FormAnswer.user_last_answer(technical_name, user)
        except RuntimeError:
            return True

        now = datetime.datetime.now()
        td = now - last.datetime

        if td.total_seconds() < delay:
            return False
        return True

    @classmethod
    def user_last_answer(cls, technical_name: str, user: User):
        r = FormAnswer.query.filter(
            FormAnswer.form_technical_name == technical_name, FormAnswer.user_id == user.id).order_by(
            FormAnswer.id.desc()).first()
        if r is None:
            raise RuntimeError("User answer not found")
        return r

    @classmethod
    def new(cls, technical_name: str, user: User, answer_data_cls: BaseModel):
        ip = request.remote_addr
        location = IpPosition(ip=ip)
        new = cls(user_id=user.id, form_technical_name=technical_name, form_data=answer_data_cls.dict(),
                  ip=ip, location=location.get_user_format(), processed_status="WAIT")
        db.session.add(new)
        db.session.commit()
        return new

    @classmethod
    def get_from_id(cls, identification: int):
        r = cls.query.order_by(FormAnswer.id.desc()).filter(cls.id == identification).first()
        if r is None:
            raise ValueError("Unknown answer")
        return r

    @classmethod
    def get_all_user_answers(cls, user, limit: int = 10):
        return cls.query.filter(cls.user_id == user.id).order_by(FormAnswer.id.desc()).limit(limit).all()
