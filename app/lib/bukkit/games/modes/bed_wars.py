import datetime

from pydantic import BaseModel

from app.lib.bukkit.games.types import BedWarsGames
from app.lib.bukkit.models.bedwars_statistics import BedwarsStatistics
from app.lib.cache import Cache

ALLOW_MODES = [mode for mode in BedWarsGames]


class BedWarsDataClass(BaseModel):
    wins: int
    kills: int
    deaths: int
    beds_destructed: int
    games: int


class BedWarsPlayerStatistics:
    def __init__(self, uuid):
        self.uuid = uuid

        self.__cache = Cache(f"bedwars_{self.uuid}")
        self._modes = {}

        if self.__cache.exist is True:
            for game_mod in ALLOW_MODES:
                try:
                    self._modes[game_mod.value] = BedWarsDataClass.parse_obj(self.__cache.get(game_mod.value))
                except:
                    continue

            return
        self.__cache.set_global_lifetime(datetime.timedelta(hours=6))

        bw_raws: list[BedwarsStatistics] = BedwarsStatistics.get_from_uuid(self.uuid)
        for bw_raw in bw_raws:
            if not bw_raw.game_section:
                continue

            mod: BedWarsGames = BedWarsGames(bw_raw.game_section.lower())
            self._modes[mod.value] = BedWarsDataClass(
                wins=bw_raw.wins,
                kills=bw_raw.kills,
                beds_destructed=bw_raw.beds_destructed,
                games=bw_raw.games,
                deaths=bw_raw.deaths)

        for mod, data in self._modes.items():
            self.__cache.set(mod, data.dict())

    def get_from_mode(self, mode) -> BedWarsDataClass:
        r = self._modes.get(mode.value, None)
        if r is None:
            return BedWarsDataClass(wins=-1,
                                    kills=-1,
                                    beds_destructed=-1,
                                    games=-1,
                                    deaths=-1)

        return BedWarsDataClass.parse_obj(r)

