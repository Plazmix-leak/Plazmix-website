from app import db
from app.helper.decorators.database import manage_session

from ._interface import IBukkitPlayerModel


class Auth(db.Model, IBukkitPlayerModel):
    __bind_key__ = 'bukkit'
    uuid = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    address = db.Column(db.String(100))
    password = db.Column(db.String(100))


    def set_new_password(self, hash_password):
        self.password = hash_password
        db.session.commit()

    @classmethod
    def get_from_uuid(cls, uuid: str):
        return cls.query.filter(cls.uuid == uuid).first()


    @classmethod
    def new(cls, uuid, address, pwd):
        new = cls(uuid=uuid,
                  address=address,
                  password=pwd)
        db.session.add(new)
        db.session.commit()
        return new
