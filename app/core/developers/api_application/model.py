import datetime
import uuid

from app import db


class DeveloperApiApplication(db.Model):
    __bind_key__ = 'web'

    uuid = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(150), unique=True)
    access_level = db.Column(db.Enum('default', 'partner', 'private'), default='default', nullable=False)
    limit = db.Column(db.Integer, default=10000, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)

    team_uuid = db.Column(
        db.String(48), db.ForeignKey('developer_team.uuid', ondelete='CASCADE')
    )
    team = db.relationship("DeveloperTeam", back_populates="api_application", uselist=False)

    @classmethod
    def get_from_uuid(cls, app_uuid):
        r = cls.query.filter(cls.uuid == app_uuid).first()
        if r is None:
            raise ValueError("Unknown application")
        return r

    def update_config(self, name=None):
        self.name = name or self.name
        db.session.commit()

    @classmethod
    def create(cls, team, name):
        if len(team.api_application) >= 5:
            raise RuntimeError("Limit")

        token = f"{uuid.uuid4().hex}-{uuid.uuid4().hex}-{uuid.uuid4().hex}"
        app_uuid = uuid.uuid4().hex

        # todo: переписать
        if team.level == 'default':
            access_level = 'default'
            limit = 10000
        elif team.level == 'partner' or team.level == 'verification_partner':
            access_level = 'partner'
            limit = 50000
        elif team.level == 'verification_partner':
            access_level = 'verification_partner'
            limit = 100000
        elif team.level == 'official':
            access_level = 'private'
            limit = 200000

        new = cls(uuid=app_uuid, token=token, access_level=access_level, team_uuid=team.uuid,
                  name=name, limit=limit)
        db.session.add(new)
        db.session.commit()
        return new

    @classmethod
    def get_from_token(cls, token: str):
        r = cls.query.filter(cls.token == token).first()
        if r is None:
            raise ValueError("Unknown application")
        return r
