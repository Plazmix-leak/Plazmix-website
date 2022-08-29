from functools import wraps

from flask import g

from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.types.error_code import ErrorType
from app.core.permissions import Permissions
from app.core.user.module import UserAuthSession


def check_admin_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_session: UserAuthSession = g.session
        if user_session is None:
            user_session: UserAuthSession = UserAuthSession.get_session_or_none()

        if user_session is None:
            raise ApiDefaultError(comment="You not authorized", error_type=ErrorType.UNAUTHORIZED)

        if Permissions.check(Permissions.PANEL_ACCESS, user_session.user) is False:
            raise ApiDefaultError(comment="Not enough rights", error_type=ErrorType.FORBIDDEN)
        kwargs['user_session'] = user_session

        return func(*args, **kwargs)
    return wrapper
