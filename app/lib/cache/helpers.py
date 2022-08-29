import datetime
from functools import wraps

from app.lib.cache import Cache


def cached_class_function_result(class_uniq_attribute, lifetime: datetime.timedelta = datetime.timedelta(minutes=15)):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            self = kwargs.get('self') or args[0]
            uniq = str(getattr(self, class_uniq_attribute))
            variable = function.__name__
            cache_client = Cache(f"{self.__class__.__name__}.{variable}.{uniq}")

            cached = cache_client.get(variable, None)
            if cached is None:
                function_result = function(*args, **kwargs)
                cache_client.set("function_result", function_result)
                cache_client.set_global_lifetime(lifetime)
                return function_result

            return cached
        return wrapper
    return decorator

