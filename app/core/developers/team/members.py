from app import db


class DeveloperTeamMembers(db.Model):
    __bind_key__ = 'web'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)

    user_uuid = db.Column(
        db.String(48), db.ForeignKey('user.uuid', ondelete='CASCADE')
    )
    user = db.relationship("User", back_populates="developer_teams", uselist=False)

    team_uuid = db.Column(
        db.String(48), db.ForeignKey('developer_team.uuid', ondelete='CASCADE')
    )
    team = db.relationship("DeveloperTeam", back_populates="members", uselist=False)

    @classmethod
    def join_team(cls, team, user):
        team_size = team.size
        if team_size >= 5:
            raise RuntimeError("Team full")

        new = cls(user_uuid=user.uuid, team_uuid=team.uuid)
        db.session.add(new)
        db.session.commit()
        return new
