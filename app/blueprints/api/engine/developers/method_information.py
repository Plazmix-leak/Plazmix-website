import datetime

from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.types.error_code import ErrorType
from app.lib.cache import Cache


class ApplicationApiMethodInformation:
    def __init__(self, application, method_signature):
        self._cache = Cache(f"{application.namespace}_{method_signature}")
        if self._cache.exist is False:
            self._cache.set_global_lifetime(datetime.timedelta(days=7))

    @property
    def last_request_time(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._cache.get('last_request_time', 0))

    @last_request_time.setter
    def last_request_time(self, value: datetime.datetime):
        self._cache.set('last_request_time', value.timestamp())

    def now_request(self):
        self.last_request_time = datetime.datetime.now()

    def access(self, method_limit):
        access_method = datetime.datetime.now() + method_limit
        if self.last_request_time > access_method:
            raise ApiDefaultError(comment="This method has a time limit, please read the documentation",
                                  error_type=ErrorType.FORBIDDEN)
