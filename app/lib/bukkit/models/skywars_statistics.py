from app import db
from app.lib.bukkit.models._interface import IBukkitPlayerModel


class SkywarsStatistics(db.Model, IBukkitPlayerModel):
    __bind_key__ = 'bukkit'

    uuid = db.Column(db.String(50), nullable=False, primary_key=True)
    game_section = db.Column(db.String(50), primary_key=True)
    wins = db.Column(db.Integer)
    kills = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    games = db.Column(db.Integer)

    @classmethod
    def get_from_uuid(cls, identification: str):
        return cls.query.filter(cls.uuid == identification).all()
