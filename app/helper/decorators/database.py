from functools import wraps

from app import db


def manage_session(bind="web"):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                db.session.execute("SELECT 1;", bind=bind)
                db.session.commit()
            except Exception as ex:
                db.session.rollback()

            try:
                res = function(*args, **kwargs)
                return res
            except Exception as e:
                db.session.rollback()
                raise e

        return wrapper

    return decorator
