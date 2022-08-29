import datetime
from enum import Enum

from app import db


class ExtServicesCode(Enum):
    VK = "vk"
    DISCORD = "discord"


class UserExternalService(db.Model):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())

    service_name = db.Column(db.String(40), default="unknown")
    user = db.relationship("User", back_populates="ext_services", uselist=False)

    user_id_service = db.Column(db.String(100))
    user_nickname_service = db.Column(db.String(100))
    service_metadata = db.Column(db.JSON)
    visible = db.Column(db.Boolean, default=1)


    def set_visible(self):
        self.visible = 1
        db.session.commit()

    def set_unvisible(self):
        self.visible = 0
        db.session.commit()

    @classmethod
    def get_user_service(cls, user, service_code: ExtServicesCode):
        r = cls.query.filter(cls.user_id == user.id, cls.service_name == service_code.value).first()
        if r is None:
            raise RuntimeError("User ext service not created")
        return r

    @classmethod
    def create_new_or_replace(cls, user, service_code: ExtServicesCode, user_id_service: str,
                              user_nickname_service: str, service_metadata: dict):
        record = cls.query.filter(cls.user_id == user.id, cls.service_name == service_code.value).first()
        if record is None:
            record = cls(user_id=user.id, service_name=service_code.value)
            db.session.add(record)

        try:
            record.user_id_service = user_id_service
            record.user_nickname_service = user_nickname_service
            record.service_metadata = service_metadata
            db.session.commit()
        except:
            db.session.rollback()
            record.user_id_service = user_id_service
            record.user_nickname_service = str(service_metadata["username"].encode('utf-8'))
            record.service_metadata = dict()
            db.session.commit()

        return record

    @classmethod
    def get_from_service_account_id(cls, service_code: ExtServicesCode, account_id: str):
        r = cls.query.filter(cls.service_name == service_code.value, cls.user_id_service == account_id).first()
        if r is None:
            raise RuntimeError("Not found")
        return r

    @classmethod
    def get_from_id(cls, ident: int):
        r = cls.query.filter(cls.id == ident).first()
        if r is None:
            raise RuntimeError("Not found")
        return r
