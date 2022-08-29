from app import db
from app.helper.decorators.database import manage_session

from ._interface import IBukkitPlayerModel


class Identifiers(db.Model, IBukkitPlayerModel):
    __bind_key__ = 'bukkit'

    identifier = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(16), unique=True)

    @classmethod
    @manage_session("bukkit")
    def get_from_username(cls, username: str):
        return cls.query.filter(cls.name == username).first()

    @classmethod
    @manage_session("bukkit")
    def get_from_uuid(cls, uuid: str):
        return cls.query.filter(cls.identifier == uuid).first()

    @classmethod
    def get_from_like_nickname(cls, nickname, page=1, limit=15):
        return cls.query.filter(cls.name.like(f"%{nickname}%")).paginate(page=page, max_per_page=limit).items

    @classmethod
    def new(cls, identification: str, nickname: str):
        new = cls(identifier=identification,
                  name=nickname)
        db.session.add(new)
        db.session.commit()
        return new

