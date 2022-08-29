from enum import Enum

from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.lib.clarence.sorted.type import CheckType


class MetricData:
    def __init__(self, check_type: CheckType, access_level: ApiAccessLevel):
        self.check_type = check_type
        self.api_access_level = access_level


class MetricAvailableCollection(Enum):
    api = MetricData(CheckType.SUM, ApiAccessLevel.VERIFICATION_PARTNER)
    accounts_total = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)
    accounts_new = MetricData(CheckType.SUM, ApiAccessLevel.DEFAULT)
    joins = MetricData(CheckType.SUM, ApiAccessLevel.PARTNER)

    online_summary_total = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)
    online_summary_hub = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)
    online_summary_lobby = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)
    online_summary_game_server = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)
    online_summary_technical = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)
    online_summary_sky_wars = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)
    online_summary_bed_wars = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)

    online_auth = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)
    online_hub = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)
    online_bwlobby = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)
    online_swlobby = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)
    online_sws = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)
    online_rsw = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)
    online_bws = MetricData(CheckType.MAX, ApiAccessLevel.DEFAULT)

    @classmethod
    def get_from_name(cls, name: str):
        for element in cls:
            if element.name == name:
                return element
        raise ValueError("Unknown element")

