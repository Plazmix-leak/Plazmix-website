import datetime
import os
import random
import string

import jwt
from flask import request, session
from jwt import DecodeError

from app import db
from .logs import UserAuthLogs
from app.lib.ip_position import IpPosition

_SESSION_KEY = "quardex.auth.jwt"


def _generate_session():
    a = string.ascii_letters + string.punctuation + string.digits
    a_len = len(a) - 1
    result = ""
    for _ in range(50):
        result += a[random.randint(0, a_len)]
    return result


class UserAuthSession(db.Model):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    token = db.Column(db.String(50))
    auth_type = db.Column(db.Enum("server", "site", "api", "unknown"), default="unknown")
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship("User", back_populates="auth_sessions", uselist=False)
    user_ip = db.Column(db.String(50))
    user_location = db.Column(db.String(200), nullable=True)

    def kill(self):
        db.session.delete(self)
        db.session.commit()
        session[_SESSION_KEY] = "logout"

    @classmethod
    def new_session(cls, user, auth_type="site"):
        from app.task.email import email_user_login
        token = _generate_session()
        jwt_token = jwt.encode({"token": token,
                                "uuid": user.uuid},
                               os.getenv('JWT_SECRET'),
                               algorithm="HS256")
        user_ip = request.remote_addr
        user_position = IpPosition(user_ip)
        new_session = cls(user_id=user.id,
                          user_ip=user_ip,
                          user_location=user_position.get_user_format(),
                          auth_type=auth_type, token=token)

        db.session.add(new_session)
        db.session.commit()
        session[_SESSION_KEY] = jwt_token

        if user.email is not None:
            email_user_login.apply_async(
                kwargs={"user_uuid": user.uuid, "ip": user_ip},
                ignore_result=True)

        UserAuthLogs.create_new(user, "site")

        return new_session

    def __eq__(self, other):
        return self.token == other.token

    @classmethod
    def get_session_or_none(cls):
        try:
            user_jwt = session[_SESSION_KEY]
        except KeyError:
            user_jwt = None

        if user_jwt is None:
            return None

        try:
            payload = jwt.decode(user_jwt, os.getenv('JWT_SECRET'), algorithms=["HS256"])
        except DecodeError:
            return None

        user_token = payload.get('token')

        active_session = cls.query.filter(cls.token == user_token).first()
        if not active_session:
            return None

        if active_session.user.uuid != payload.get('uuid'):
            return None

        return active_session
