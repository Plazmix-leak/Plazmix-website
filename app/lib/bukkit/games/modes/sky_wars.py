import datetime

from pydantic import BaseModel

from app.lib.bukkit.games.types import SkyWarsGames
from app.lib.bukkit.models.skywars_statistics import SkywarsStatistics
from app.lib.cache import Cache

ALLOW_MODES = [mode for mode in SkyWarsGames]


class SkyWarsDataClass(BaseModel):
    wins: int
    kills: int
    assists: int
    games: int


class SkyWarsPlayerStatistics:
    def __init__(self, uuid):
        self.uuid = uuid

        self.__cache = Cache(f"skywars_{self.uuid}")
        self._modes = {}

        if self.__cache.exist is True:
            for game_mod in ALLOW_MODES:
                try:
                    self._modes[game_mod.value] = SkyWarsDataClass.parse_obj(self.__cache.get(game_mod.value))
                except:
                    continue

            return
        self.__cache.set_global_lifetime(datetime.timedelta(hours=6))

        sw_raws: list[SkywarsStatistics] = SkywarsStatistics.get_from_uuid(self.uuid)
        for sw_raw in sw_raws:
            if not sw_raw.game_section:
                continue

            mod: SkyWarsGames = SkyWarsGames(sw_raw.game_section.lower())
            self._modes[mod.value.lower()] = SkyWarsDataClass(
                wins=sw_raw.wins,
                kills=sw_raw.kills,
                assists=sw_raw.assists,
                games=sw_raw.games)

        for mod, data in self._modes.items():
            self.__cache.set(mod, data.dict())

    def get_from_mode(self, mode) -> SkyWarsDataClass:
        r = self._modes.get(mode.value.lower(), None)
        if r is None:
            return SkyWarsDataClass(wins=-1,
                                    kills=-1,
                                    assists=-1,
                                    games=-1)

        return SkyWarsDataClass.parse_obj(r)

