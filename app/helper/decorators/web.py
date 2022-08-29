from functools import wraps

from flask import redirect, url_for, g, request


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if g.session is None or g.user is None:
            return redirect(url_for("auth.login") + f"?next={request.url}")
        return function(*args, **kwargs)
    return wrapper

