import datetime
import uuid

from app import db
from .members import DeveloperTeamMembers


class DeveloperTeam(db.Model):
    __bind_key__ = 'web'

    uuid = db.Column(db.String(50), unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String(50))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)

    level = db.Column(db.Enum('default', 'partner', 'verification_partner', 'official'),
                      default='default', nullable=False)

    members = db.relationship("DeveloperTeamMembers", back_populates="team", cascade="all, delete-orphan")

    oauth_application = db.relationship("OauthApplication", back_populates="team")
    api_application = db.relationship("DeveloperApiApplication", back_populates="team")

    @property
    def size(self):
        return len(self.members)

    @classmethod
    def create(cls, user, name):
        team_uuid = uuid.uuid4().hex
        new_team = DeveloperTeam(uuid=team_uuid, name=name)
        db.session.add(new_team)
        db.session.commit()
        DeveloperTeamMembers.join_team(new_team, user)
        return new_team

    def user_can_member(self, user):
        for member in self.members:
            if user.uuid == member.user_uuid:
                return True
        return False

    @classmethod
    def get_from_uuid(cls, ident: str):
        r = cls.query.filter(cls.uuid == ident).first()
        if r is None:
            raise ValueError("Unknown team")
        return r
