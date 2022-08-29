from app import db
from app.blueprints.gift.engine.models.data_class import UserGiftDataClass


class UserGift(db.Model):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    gift_uuid = db.Column(db.String(50), db.ForeignKey('gift.uuid'))
    user_id = db.Column(db.Integer, nullable=False)
    open = db.Column(db.Boolean, default=False)

    gift = db.relationship("Gift", back_populates="users", uselist=False)

    def opened(self):
        self.open = True
        db.session.commit()

    @property
    def data_class(self) -> UserGiftDataClass:
        gift_type, gift_author = self.gift.impl.author_info
        return UserGiftDataClass(open=self.open,
                                 author_name=gift_author if gift_type == 'special' else gift_author.bukkit.nickname,
                                 name=self.gift.name)

    @classmethod
    def add_gift_in_user(cls, user, gift):
        new = cls(gift_uuid=gift.uuid, user_id=user.id)
        db.session.add(new)
        db.session.commit()

    @classmethod
    def get_from_id(cls, identification):
        r = cls.query.get(identification)
        if r is None:
            raise ValueError("Unknown gift")
        return r

    @classmethod
    def get_all_from_user(cls, user):
        return cls.query.filter(cls.user_id == user.id).all()
