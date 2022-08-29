import datetime
from flask import request

from app import db
from app.lib.ip_position import IpPosition


class UserAuthLogs(db.Model):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="auth_logs", uselist=False)

    datetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    service = db.Column(db.Enum('site', 'server', 'unknown'), default='unknown')

    ip = db.Column(db.String(50))
    ip_location = db.Column(db.Text, nullable=True)

    @classmethod
    def get_from_user(cls, user, count=150):
        return cls.query.order_by(cls.id.desc()).filter(cls.user_id == user.id).limit(count)

    @classmethod
    def create_new(cls, user, service, ip=None):
        user_ip = ip or request.remote_addr
        user_position = IpPosition(user_ip)
        new = cls(user_id=user.id,
                  service=service,
                  ip=user_ip,
                  ip_location=user_position.get_user_format())

        db.session.add(new)
        db.session.commit()
        return new

