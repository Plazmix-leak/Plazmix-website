import datetime
from functools import wraps
from typing import List

from app.blueprints.api.engine.api_class.method.method import ApiClassMethod
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.request import RequestType


def api_method(request_methods: List[RequestType] = None, cooldown: datetime.timedelta = None,
               access_level: ApiAccessLevel = None, query_data_class=None, response_check=True):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            api_cls = kwargs.get('self', None) or args[0]

            api_class_method = ApiClassMethod(api_cls=api_cls,
                                              method=function, request_methods=request_methods,
                                              blocked_time=cooldown, access_level=access_level,
                                              request_data_class=query_data_class,
                                              response_check=response_check)
            return api_class_method
        return wrapper
    return decorator
