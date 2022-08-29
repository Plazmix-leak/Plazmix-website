import datetime

from pydantic import BaseModel

from app import db
from app.core.user import User
from app.core.panel.types import ModeratorAlertType


class ModeratorAlertDataClass(BaseModel):
    id: int
    author: str
    type: str
    reason: str
    create_date_timestamp: float
    active: bool


class ModeratorAlert(db.Model):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    to = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Enum("reprimand", "warning"))
    reason = db.Column(db.Text)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    is_active = db.Column(db.Boolean, default=1)

    @property
    def data_model(self):
        return ModeratorAlertDataClass(id=self.id,
                                       author=self.author,
                                       type=self.type,
                                       reason=self.reason,
                                       create_date_timestamp=self.create_date.timestamp(),
                                       active=self.is_active)

    @property
    def author_user(self):
        return User.get_from_uuid(self.author)

    @property
    def to_user(self):
        return User.get_from_uuid(self.to)

    @property
    def type_rus(self):
        status = ModeratorAlertType(self.type)
        if status == ModeratorAlertType.REPRIMAND:
            return "Выговор"
        elif status == ModeratorAlertType.WARNING:
            return "Предупреждение"
        return "Неизвестный"

    def deactivate(self):
        self.is_active = False
        db.session.commit()

    def activate(self):
        self.is_active = True
        db.session.commit()

    @classmethod
    def create(cls, author, to, reason, alert_type: ModeratorAlertType):
        new = cls(author=author.uuid, to=to.uuid, reason=reason, type=alert_type.value)
        db.session.add(new)
        db.session.commit()

    @classmethod
    def get_from_id(cls, identification: int):
        r = cls.query.filter(cls.id == identification).first()
        if r is None:
            raise ValueError("Unknown warning")
        return r

    @classmethod
    def get_all_to(cls, to, alert_type: ModeratorAlertType):
        r = cls.query.filter(cls.to == to.uuid, cls.type == alert_type.value).all()
        # sorted(r, key=lambda x: x.is_active, reverse=True)
        return sorted(r, key=lambda x: x.is_active, reverse=True)
