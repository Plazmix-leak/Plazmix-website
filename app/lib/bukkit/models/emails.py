from app import db
from app.helper.decorators.database import manage_session

from ._interface import IBukkitPlayerModel


class Emails(db.Model, IBukkitPlayerModel):
    __bind_key__ = 'bukkit'

    uuid = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True)

    def update_email(self, new_email):
        self.email = new_email
        db.session.commit()

    @classmethod
    def create_from_uuid(cls, uuid, email):
        new = cls(uuid=uuid, email=email)
        db.session.add(new)
        db.session.commit()
        return new

    @classmethod
    @manage_session("bukkit")
    def get_from_uuid(cls, uuid: str):
        return cls.query.filter(cls.uuid == uuid).first()
