import datetime
from functools import wraps

from flask import g, abort

from .rules import Rules
from .permissions import Permissions
from app.lib.cache import Cache


def rule_access_check(rule: Rules):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if g.user is None:
                return abort(401)

            cache = Cache(f"rule_access_check_decorator_{g.user.uuid}")

            if cache.exist is False:
                cache.set_global_lifetime(datetime.timedelta(days=1))

            cached_result = cache.get(str(rule))

            if cached_result is True:
                return function(*args, **kwargs)

            perm_result = Permissions.check(rule, user=g.user)
            cache.set(str(rule), perm_result)
            if perm_result is False:
                return abort(403)

            return function(*args, **kwargs)
        return wrapper
    return decorator

