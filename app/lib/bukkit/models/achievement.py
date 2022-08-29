from app import db

from ._interface import IBukkitPlayerModel


class Achievements(db.Model, IBukkitPlayerModel):
    __bind_key__ = 'bukkit'
    uuid = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    achievements = db.Column(db.Text)

    @classmethod
    def get_from_uuid(cls, uuid: str):
        return cls.query.filter(cls.uuid == uuid).first()
