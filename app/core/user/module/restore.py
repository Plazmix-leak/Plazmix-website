import datetime
import uuid

from flask import url_for

from app import db


class UserPasswordRestore(db.Model):
    __bind_key__ = 'web'

    uuid = db.Column(db.String(50), primary_key=True, unique=True,
                     nullable=False, default=uuid.uuid4().hex)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    use = db.Column(db.Boolean, default=0)
    end_date = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    user = db.relationship("User", back_populates="password_restore", uselist=False)

    @property
    def link(self):
        try:
            return url_for("auth.restore_password", restore_uuid=self.uuid, _external=True)
        except RuntimeError:
            return self.uuid

    def used(self, new_password):
        self.use = True
        db.session.commit()
        self.user.edit_password(new_password)

    @property
    def is_active(self):
        now = datetime.datetime.now()
        if now < self.end_date and self.use is False:
            return True
        return False

    @classmethod
    def init_from_user(cls, user, send_email=True):

        end_active = datetime.datetime.now() + datetime.timedelta(hours=1)
        new = cls(user_id=user.id, end_date=end_active, uuid=uuid.uuid4().hex)
        db.session.add(new)
        db.session.commit()

        if send_email:
            from app.task.email import email_user_restore
            email_user_restore.apply_async(
                kwargs={"restore_uuid": new.uuid},
                ignore_result=True)

        return new

    @classmethod
    def get_from_uuid(cls, identification: str):
        restore = cls.query.filter(cls.uuid == identification).first()
        if restore is None:
            raise ValueError("Unknown restore")
        return restore
