import datetime

import humanize

from app import db
from app.core.user import User


class PageVersion(db.Model):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    public = db.Column(db.Boolean, default=False, nullable=False)
    page = db.relationship("Page", back_populates="versions", uselist=False)

    author_uuid = db.Column(db.String(50))
    public_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    title = db.Column(db.String(500), default="Unknown")
    content = db.Column(db.Text, default="<p>Пусто :(</p>")

    @property
    def author(self) -> User:
        return User.get_from_uuid(self.author_uuid)

    @property
    def human_date(self):
        if self.public_time is None:
            return "Неизвестно"

        _t = humanize.i18n.activate("ru_RU")
        return humanize.naturalday(self.public_time)

    def publish(self):
        self.public = True
        db.session.commit()

    def hide(self):
        self.public = False
        db.session.commit()

    @classmethod
    def create(cls, page_id: int, author: User, title: str, content: str):
        version = cls(author_uuid=author.uuid, public=True, page_id=page_id,
                      title=title, content=content)
        db.session.add(version)
        db.session.commit()
        return version

    @classmethod
    def get_from_id(cls, identification: int):
        r = cls.query.get(identification)
        if r is None:
            raise ValueError("Unknown version")
        return r
