from .modes import BedWarsPlayerStatistics, SkyWarsPlayerStatistics


class BukkitPlayerGame:
    def __init__(self, uuid):
        self._uuid = uuid

    @property
    def skywars_statistics(self) -> SkyWarsPlayerStatistics:
        return SkyWarsPlayerStatistics(self._uuid)

    @property
    def bedwars_statistics(self) -> BedWarsPlayerStatistics:
        return BedWarsPlayerStatistics(self._uuid)


