import textwrap

from pydantic import BaseModel

import html

from app import db
from app.lib.link import ShortLink, LinkOwnerType
from app.lib.link.enums import RedirectType


class NewsDataModel(BaseModel):
    id: int = None
    title: str = None
    image: str = None
    author: str = None
    short_text: str = None
    full_text: str = None
    more_link: str = None
    read_time: int = 0


class News(db.Model):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(50))
    author = db.Column(db.String(100))
    image_link = db.Column(db.String(400))
    short_text = db.Column(db.UnicodeText(200))
    full_text = db.Column(db.UnicodeText(1000))
    more_link = db.Column(db.String(300), nullable=True)

    @property
    def data_model(self) -> NewsDataModel:
        return NewsDataModel(id=self.id, title=self.title, author=self.author,
                             short_text=self.parse_short_text, full_text=self.parse_text,
                             more_link=self.more_link,
                             image=self.image_link,
                             read_time=self.read_time)

    @property
    def read_time(self):
        return int((len(self.full_text)/100) + 0.5)

    @classmethod
    def get_last(cls, count: int):

        return db.session.query(cls).order_by(cls.id.desc()).limit(count).all()

    @property
    def parse_text(self) -> str:
        return html.unescape(self.full_text)

    @property
    def parse_short_text(self) -> str:
        return html.unescape(self.short_text)

    @property
    def parse_title(self) -> str:
        return html.unescape(self.title)

    @classmethod
    def create(cls, text, author, title=None, more=None, image=None):
        short_text = textwrap.shorten(text, width=97, placeholder="...")
        title = title or textwrap.shorten(text, width=20, placeholder="")
        new = cls(title=title, author=author, full_text=text,
                  short_text=short_text, more_link=more, image_link=image)
        db.session.add(new)
        db.session.commit()
        if more is not None:
            new.more_link = ShortLink.create_link(LinkOwnerType.SYSTEM, f"news-{new.id}",
                                                  more, redirect_type=RedirectType.SPEED).urls[1]
            db.session.commit()
        return new

    @classmethod
    def create_from_model(cls, model: NewsDataModel):
        return cls.create(model.full_text, author=model.author, title=model.author,
                          more=model.more_link, image=model.image)

    @classmethod
    def get_from_id(cls, identification: int):
        r = cls.query.filter(cls.id == identification).first()
        if r is None:
            raise ValueError()
        return r

