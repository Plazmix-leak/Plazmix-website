from functools import wraps

from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.types.error_code import ErrorType
from app.core.user import User


def get_user(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')
        try:
            if query.id is not None:
                user: User = User.get_from_id(query.id)
            elif query.uuid is not None:
                user: User = User.get_from_uuid(query.uuid)
            elif query.nickname is not None:
                user: User = User.get_from_nickname(query.nickname)
            else:
                raise ApiDefaultError(comment="You have not specified any of the necessary parameters",
                                      error_type=ErrorType.BAD_SYNTAX)
        except ValueError:
            raise ApiDefaultError(comment="User not found",
                                  error_type=ErrorType.USER_NOT_FOUND)
        kwargs["player"] = user

        return function(*args, **kwargs)
    return wrapper
