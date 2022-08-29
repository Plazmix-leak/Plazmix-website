import datetime

import humanize

from app.lib.bukkit.models import Auth
from app.lib.cache import Cache, FileCacheStorage


class BukkitServerInfo:
    def __init__(self):
        self._cache = Cache(self.__class__.__name__, FileCacheStorage)
        if self._cache.exist is False:
            self._cache.set_global_lifetime(datetime.timedelta(hours=3))

    @property
    def account_count_human(self):
        return humanize.intcomma(self.get_account_count())

    def get_account_count(self, update_cache=False):
        cached_result = self._cache.get("get_account_count")
        if cached_result and update_cache is False:
            return cached_result
        count = Auth.query.count()
        self._cache.set("get_account_count", count)
        return count

