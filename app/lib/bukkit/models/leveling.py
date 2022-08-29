from app import db
from app.helper.decorators.database import manage_session

from ._interface import IBukkitPlayerModel


class Leveling(db.Model, IBukkitPlayerModel):
    __bind_key__ = 'bukkit'

    uuid = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    level = db.Column(db.Integer)

    @classmethod
    @manage_session("bukkit")
    def get_from_uuid(cls, uuid: str):
        return cls.query.filter(cls.uuid == uuid).first()
