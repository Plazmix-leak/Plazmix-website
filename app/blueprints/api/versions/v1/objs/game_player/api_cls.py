from abc import ABC

from app.blueprints.api.engine.api_class.interface import IApiClass
from app.blueprints.api.engine.api_class.method.decorator import api_method
from app.blueprints.api.engine.api_class.method.result import ApiMethodResult
from app.blueprints.api.engine.api_class.settings import ApiClassSettings
from app.blueprints.api.engine.request import ApiRequest
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.request import RequestType
from app.blueprints.api.versions.v1.objs.user.data_class.request import UserGetRequest
from app.blueprints.api.versions.v1.objs.user.helpers import get_user
from app.core.user import User as Plazmix
from app.lib.bukkit.games import SkyWarsGames, BedWarsGames


class GameUser(IApiClass, ABC):
    def settings(self) -> ApiClassSettings:
        return ApiClassSettings(access_level=ApiAccessLevel.DEFAULT)

    @api_method(request_methods=[RequestType.POST], query_data_class=UserGetRequest)
    @get_user
    def getSkyWarsStatistics(self, request: ApiRequest, query: UserGetRequest, player: Plazmix):
        sky_wars = player.bukkit.game.skywars_statistics
        result = {}
        for sw_game_type in SkyWarsGames:
            result[sw_game_type.value] = sky_wars.get_from_mode(sw_game_type).dict()
        return ApiMethodResult(response=result, request_type=RequestType.POST)

    @api_method(request_methods=[RequestType.POST], query_data_class=UserGetRequest)
    @get_user
    def getBedWarsStatistics(self, request: ApiRequest, query: UserGetRequest, player: Plazmix):
        bed_wars = player.bukkit.game.bedwars_statistics
        result = {}
        for bw_game_type in BedWarsGames:
            result[bw_game_type.value] = bed_wars.get_from_mode(bw_game_type).dict()
        return ApiMethodResult(response=result, request_type=RequestType.POST)
