import datetime
import uuid

from flask import url_for

from app import db
from app.core.user.user import User


class EditEmail(db.Model):
    __bind_key__ = 'web'

    uuid = db.Column(db.String(50), primary_key=True, unique=True,
                     nullable=False, default=uuid.uuid4().hex)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    use = db.Column(db.Boolean, default=0)
    end_date = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    new_email = db.Column(db.String(300))
    user = db.relationship("User", back_populates="email_edit", uselist=False)

    @property
    def link(self):
        try:
            return url_for("profile.email_edit", email_edit_uuid=self.uuid, _external=True)
        except RuntimeError:
            return self.uuid

    def used(self):
        self.use = True
        db.session.commit()
        self.user.edit_email(self.new_email)

    @property
    def is_active(self):
        now = datetime.datetime.now()
        if now < self.end_date and self.use is False:
            return True
        return False

    @classmethod
    def init_from_user(cls, user: User, new_email):
        from app.task.email import email_validate

        try:
            User.get_from_email(new_email)
            raise RuntimeError()
        except ValueError:
            pass

        end_active = datetime.datetime.now() + datetime.timedelta(hours=1)
        new = cls(user_id=user.id, end_date=end_active, uuid=uuid.uuid4().hex, new_email=new_email)
        db.session.add(new)
        db.session.commit()

        email_validate.apply_async(
                kwargs={"edit_uuid": new.uuid},
                ignore_result=True)

        return new

    @classmethod
    def get_from_uuid(cls, identification: str):
        restore = cls.query.filter(cls.uuid == identification).first()
        if restore is None:
            raise ValueError("Unknown email edit")
        return restore
