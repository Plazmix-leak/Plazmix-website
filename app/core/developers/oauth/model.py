import datetime
import time

import uuid
from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin, OAuth2AuthorizationCodeMixin, OAuth2TokenMixin
from werkzeug.security import gen_salt

from app import db


class OauthToken(db.Model, OAuth2TokenMixin):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_uuid = db.Column(
        db.String(48), db.ForeignKey('user.uuid', ondelete='CASCADE')
    )
    user = db.relationship("User", back_populates="oauth_tokens", uselist=False)


class OauthApplication(db.Model, OAuth2ClientMixin):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    team_uuid = db.Column(
        db.String(48), db.ForeignKey('developer_team.uuid', ondelete='CASCADE')
    )
    create_date = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    team = db.relationship("DeveloperTeam", back_populates="oauth_application", uselist=False)

    @classmethod
    def generate_new_app(cls, team, name):
        if len(team.oauth_application) >= 5:
            raise RuntimeError("Limit")

        new = cls(team_uuid=team.uuid, client_id_issued_at=int(time.time()),
                  client_id=uuid.uuid4().hex, name=name,
                  client_secret=gen_salt(48))
        db.session.add(new)
        db.session.commit()
        return new

    @classmethod
    def get_from_client_id_info(cls, client_id_info):
        r = cls.query.filter(cls.client_id == client_id_info).first()
        if r is None:
            raise ValueError("Unknown oauth app")
        return r

    def update_config(self, name, metadata):
        self.name = name
        db.session.commit()
        self.set_client_metadata(metadata)


class OauthAuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_uuid = db.Column(
        db.String(48), db.ForeignKey('user.uuid', ondelete='CASCADE')
    )
    user = db.relationship("User", back_populates="oauth_auth_codes", uselist=False)
