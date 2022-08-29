import datetime

from app import redis_client
from app.core.developers.api_application import DeveloperApiApplication as DeveloperApplicationModel
from app.blueprints.api.engine.developers.method_information import ApplicationApiMethodInformation
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.lib.cache import Cache


class DeveloperApplication:
    def __init__(self, access_level: ApiAccessLevel, uuid: str, limit: int):
        self._access_level = access_level
        self._uuid = uuid
        self._limit = limit

    @property
    def access_level(self):
        return self._access_level

    @property
    def namespace(self):
        return f"dev_app_{self._uuid}"

    @property
    def time_to_end(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(redis_client.pttl(self.namespace))

    def get_method_information(self, method_signature) -> ApplicationApiMethodInformation:
        return ApplicationApiMethodInformation(self, method_signature=method_signature)

    def get_usage(self):
        def __generate():
            redis_client.set(self.namespace, 0)
            redis_client.expire(self.namespace, int(datetime.timedelta(hours=24).total_seconds()))

        try:
            usage = int(redis_client.get(self.namespace).decode('utf-8'))
        except (AttributeError, TypeError):
            __generate()
            usage = 0

        if usage is None:
            __generate()

        return usage or 0

    def can_use(self):
        if self._limit == -1:
            return True
        return int(self.get_usage()) <= int(self._limit)

    def new_use(self):
        redis_client.incr(self.namespace, 1)

    @classmethod
    def get_from_token(cls, token):
        cache = Cache(f"da_{token}")

        def __update_data():
            model_result: DeveloperApplicationModel = DeveloperApplicationModel.get_from_token(token)
            cache.set('access_level', model_result.access_level)
            cache.set('uuid', model_result.uuid)
            cache.set('limit', model_result.limit)
            cache.set_global_lifetime(datetime.timedelta(hours=12))

        if cache.exist is False:
            try:
                __update_data()
            except ValueError:
                raise RuntimeError()
            cache.set_global_lifetime(datetime.timedelta(hours=24))

        access_level = ApiAccessLevel.get_from_technical_name(cache.get('access_level'))
        uuid = cache.get('uuid')
        limit = cache.get('limit')

        if access_level is None or uuid is None or limit is None:
            __update_data()
            access_level = ApiAccessLevel.get_from_technical_name(cache.get('access_level'))
            uuid = cache.get('uuid')
            limit = cache.get('limit')

        return cls(access_level=access_level, uuid=uuid, limit=limit)
