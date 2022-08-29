import datetime
import uuid as uuid

from sqlalchemy import desc

from app import db
from app.blueprints.gift.engine.specail_author import SpecialAuthor


class Gift(db.Model):
    __bind_key__ = 'web'

    uuid = db.Column(db.String(50), primary_key=True, unique=True, nullable=False, default=uuid.uuid4().hex)
    use_link = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    usage = db.Column(db.Integer, default=0)
    name = db.Column(db.String(300), default="Без имени")
    author_uuid = db.Column(db.String(50), default="unknown")
    link_usage_limit = db.Column(db.Integer, default=0)
    technical_name = db.Column(db.String(50), default="unknown")
    creation_date = db.Column(db.DateTime, default=datetime.datetime.now())
    data = db.Column(db.JSON)

    users = db.relationship("UserGift", back_populates="gift")

    def new_use(self):
        self.usage += 1
        db.session.commit()

    @property
    def impl(self):
        from app.blueprints.gift import GiftEngine
        return GiftEngine.get_from_models(self)

    def update(self, uuid: str, name: str, link_usage_limit: int, technical_name: str, data: dict, author_uuid: str,
               use_link: bool, active: bool):
        self.uuid = uuid
        self.name = name
        self.link_usage_limit = link_usage_limit
        self.technical_name = technical_name
        self.data = data
        self.author_uuid = author_uuid
        self.use_link = use_link
        self.active = active
        db.session.commit()

    @classmethod
    def create(cls, uuid: str, name: str, link_usage_limit: int, technical_name: str, data: dict, author_uuid: str,
               use_link: bool, active: bool):
        new = cls(uuid=uuid,
                  use_link=use_link,
                  active=active,
                  usage=0,
                  name=name,
                  author_uuid=author_uuid,
                  link_usage_limit=link_usage_limit,
                  technical_name=technical_name,
                  data=data)
        db.session.add(new)
        db.session.commit()
        return new

    @classmethod
    def get_from_uuid(cls, uuid: str):
        return cls.query.filter(cls.uuid == uuid).first()

    @classmethod
    def get_from_special_author(cls, special_author: SpecialAuthor):
        return cls.query.filter(cls.author_uuid == special_author.value).order_by(desc(cls.creation_date)).all()
