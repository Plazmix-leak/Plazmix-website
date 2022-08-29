import datetime
import humanize
from flask import request

from app import db
from app.lib.ip_position import IpPosition


class UserBalanceLog(db.Model):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="balance_logs", uselist=False)

    datetime = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    comment = db.Column(db.String(300), default="Нет комментария")
    amount = db.Column(db.Integer, nullable=False)
    before_change = db.Column(db.Integer, nullable=False)
    after_change = db.Column(db.Integer, nullable=False)

    ip = db.Column(db.String(50))
    location = db.Column(db.String(200), nullable=True)

    @property
    def human_date(self):
        if self.datetime is None:
            return "Неизвестно"

        _t = humanize.i18n.activate("ru_RU")
        return humanize.naturalday(self.datetime)

    @classmethod
    def user_money_edit(cls, user, amount: int, comment: str = "Нет комменатрия"):
        before_money = user.money
        ip = request.remote_addr
        user.money = amount
        location = IpPosition(ip)

        new = cls(user_id=user.id, before_change=before_money, amount=amount, comment=comment,
                  after_change=before_money + amount,
                  ip=ip,
                  location=location.get_user_format())

        db.session.add(new)
        db.session.commit()
        if user.email:
            from app.task.email import email_wallet
            email_wallet.apply_async(
                kwargs={"log_id": new.id},
                ignore_result=True)
        return new

    @classmethod
    def get_from_user(cls, user, count):
        return UserBalanceLog.query.filter(
            UserBalanceLog.user_id == user.id).order_by(UserBalanceLog.id.desc()).limit(count)

    @classmethod
    def get_from_id(cls, identification: int):
        log = cls.query.get(identification)
        if log is None:
            raise ValueError("unknown log")
        return log

    @classmethod
    def get_last(cls, count: int):
        return db.session.query(cls).order_by(cls.id.desc()).limit(count).all()
