from app import db
from app.helper.decorators.database import manage_session

from ._interface import IBukkitPlayerModel


class Permissions(db.Model, IBukkitPlayerModel):
    __bind_key__ = 'bukkit'

    uuid = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    permissions = db.Column(db.TEXT)

    def update_permissions(self, permissions_list):
        self.permissions = permissions_list
        db.session.commit()

    @property
    def privileges(self):
        return self.permissions.split()

    @classmethod
    @manage_session("bukkit")
    def get_from_uuid(cls, uuid: str):
        return cls.query.filter(cls.uuid == uuid).first()

    @classmethod
    def get_from_group(cls, group: str):
        return cls.query.filter(cls.permissions.like(f"%{group}%")).all()

    @classmethod
    def create_new(cls, uuid: str, permissions: str):
        new = cls(uuid=uuid,
                  permissions=permissions)
        db.session.add(new)
        db.session.commit()
        return new


