from typing import List

from app import db
from .page_versions import PageVersion
from app.core.user import User


class Page(db.Model):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    uri = db.Column(db.String(150), primary_key=True, unique=True, nullable=False)
    public = db.Column(db.Boolean, default=False)

    versions = db.relationship("PageVersion", back_populates="page", cascade="all, delete-orphan")

    @property
    def current_version(self) -> PageVersion:
        versions: List[PageVersion] = self.versions
        current = None

        for ver in versions:
            if ver.public is True:
                current = ver

        if current is None:
            raise RuntimeError("No public version")

        return current

    @current_version.setter
    def current_version(self, value: PageVersion):
        for ver in self.versions:
            if ver.public is True:
                ver.hide()
        value.publish()

    def new_version(self, author: User, title, content):
        return PageVersion.create(page_id=self.id, author=author, title=title, content=content)

    def hide(self):
        self.public = False
        db.session.commit()

    def publish(self):
        self.public = True
        db.session.commit()

    @classmethod
    def get_from_id(cls, identification: int):
        r = cls.query.filter(cls.id == identification).first()
        if r is None:
            raise ValueError("Unknown page")
        return r

    @classmethod
    def get_from_uri(cls, uri):
        r = cls.query.filter(cls.uri == uri).first()
        if r is None:
            raise ValueError("Unknown page")
        return r

    @classmethod
    def create(cls, uri: str, author: User, title: str, content: str):
        page = cls(uri=uri, public=False)
        db.session.add(page)
        db.session.commit()
        version = page.new_version(author=author, title=title, content=content)
        page.current_version = version
        return page

    @classmethod
    def get_all_publish(cls):
        return cls.query.filter(cls.public == 1).all()

    @classmethod
    def get_all(cls):
        return cls.query.all()
