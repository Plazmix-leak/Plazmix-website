import datetime
from abc import ABC

from authlib.integrations.flask_oauth2 import current_token

from app.blueprints.api.engine.api_class.interface import IApiClass
from app.blueprints.api.engine.api_class.method.decorator import api_method
from app.blueprints.api.engine.api_class.method.result import ApiMethodResult
from app.blueprints.api.engine.api_class.settings import ApiClassSettings
from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.request import ApiRequest
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.error_code import ErrorType
from app.blueprints.api.engine.types.request import RequestType
from app.blueprints.api.helpers.paginate import get_from_paginate
from app.blueprints.api.versions.v1.objs.user.data_class.request import UserGetRequest, UserAllRequest, UserGetStaff, \
    UserGetExternalService
from app.blueprints.api.versions.v1.objs.user.data_class.response import AllUsersResponse, UserFriendResponse, \
    UserAchievement, UserAchievementResponse
from app.blueprints.api.versions.v1.objs.user.helpers import get_user
from app.blueprints.gift.engine.models import UserGift
from app.core.developers.oauth.ext import require_oauth
from app.core.user import User as Plazmix
from app.core.user.module.ext_services import UserExternalService, ExtServicesCode
from app.core.permissions.groups import PermissionGroups, STAFF_GROUPS
from app.lib.bukkit.achievement import BukkitAchievementSection
from app.lib.cache import Cache


class User(IApiClass, ABC):
    def settings(self) -> ApiClassSettings:
        return ApiClassSettings(access_level=ApiAccessLevel.DEFAULT)

    @api_method(request_methods=[RequestType.POST],
                cooldown=datetime.timedelta(seconds=5), query_data_class=UserGetRequest)
    @get_user
    def get(self, request: ApiRequest, query: UserGetRequest, player: Plazmix):
        return ApiMethodResult(response=player.data_model.dict(),
                               request_type=RequestType.POST)

    @api_method(request_methods=[RequestType.GET], access_level=ApiAccessLevel.PERSONAL)
    def me(self, request: ApiRequest, query):

        @require_oauth()
        def logic():
            current_user = current_token.user
            return ApiMethodResult(response=current_user.data_model.dict(),
                                   request_type=RequestType.GET)

        try:
            return logic()
        except Exception:
            raise ApiDefaultError("Only oauth2 token", error_type=ErrorType.FORBIDDEN)

    @api_method(request_methods=[RequestType.POST],
                cooldown=datetime.timedelta(seconds=5), query_data_class=UserGetRequest)
    @get_user
    def onlineStatus(self, request: ApiRequest, query: UserGetRequest, player: Plazmix):
        return ApiMethodResult(response=player.online_data_model.dict(),
                               request_type=RequestType.POST)

    @api_method(request_methods=[RequestType.POST],
                cooldown=datetime.timedelta(seconds=10), query_data_class=UserGetRequest)
    @get_user
    def friends(self, request: ApiRequest, query: UserGetRequest, player: Plazmix):
        friends = UserFriendResponse(friends=[friend.data_model for friend in player.friends])
        return ApiMethodResult(response=friends.dict(),
                               request_type=RequestType.POST)

    @api_method(request_methods=[RequestType.POST], cooldown=datetime.timedelta(seconds=15),
                access_level=ApiAccessLevel.PARTNER, query_data_class=UserAllRequest)
    def all(self, request: ApiRequest, query: UserAllRequest):
        users, paginate_response = get_from_paginate(Plazmix, query.paginate, page_limit=10)
        res = AllUsersResponse(pagination=paginate_response, users=users)
        return ApiMethodResult(request_type=RequestType.POST, response=res.dict())

    @api_method(request_methods=[RequestType.POST], query_data_class=UserGetStaff)
    def staff(self, request: ApiRequest, query: UserGetStaff):
        cache = Cache("api_user_staff")
        if cache.exist is None:
            cache.set_global_lifetime(datetime.timedelta(hours=12))

        try:
            staff_group = PermissionGroups.get_from_technical_name(query.staff_group)
        except ValueError:
            raise ApiDefaultError(comment="Unknown group", error_type=ErrorType.BAD_SYNTAX)

        cached = cache.get(staff_group.value.get_technical_name, None)
        if cached is not None:
            return ApiMethodResult(request_type=RequestType.POST,
                                   response=cached)

        check = False
        for ag in STAFF_GROUPS:
            if staff_group.value == ag.value:
                check = True
                break

        if check is False:
            raise ApiDefaultError(comment="Is not staff group", error_type=ErrorType.BAD_SYNTAX)

        staff = Plazmix.get_all_user_from_group(staff_group)
        response = {'staffs': [user.data_model.dict(exclude={'online'}) for user in staff]}
        cache.set(staff_group.value.get_technical_name, response)
        return ApiMethodResult(response=response, request_type=RequestType.POST)

    @api_method(request_methods=[RequestType.POST], query_data_class=UserGetRequest)
    @get_user
    def getGifts(self, request: ApiRequest, query: UserGetRequest, player: Plazmix):
        user_gifts = UserGift.get_all_from_user(player)
        return ApiMethodResult(response={"gifts": [gift.data_class.dict() for gift in user_gifts]},
                               request_type=RequestType.POST)

    @api_method(request_methods=[RequestType.POST], query_data_class=UserGetRequest)
    @get_user
    def achievements(self, request: ApiRequest, query: UserGetRequest, player: Plazmix):
        result = []
        achievements = player.bukkit.achievements
        count = 0
        total = 0

        secret_count = 0

        for achievement in achievements:
            total += 1
            try:
                date_str = achievement.received_time.timestamp()
                count += 1
            except RuntimeError:
                date_str = 0.0

            technical_name = achievement.achievement.name
            if achievement.achievement.value.section == BukkitAchievementSection.SECRET:
                secret_count += 1
                technical_name = f"SECRET_ACHIEVEMENT_{secret_count}"

            data = UserAchievement(technical_name=technical_name,
                                   received=achievement.can_received,
                                   section=achievement.achievement.value.section.name,
                                   description=achievement.achievement.value.description,
                                   level=achievement.level,
                                   received_time=date_str)
            result.append(data)

        response_data = UserAchievementResponse(achievements=result,
                                                received_count=count,
                                                total_count=total)

        return ApiMethodResult(response=response_data.dict(),
                               request_type=RequestType.POST)

    @api_method(request_methods=[RequestType.POST],
                access_level=ApiAccessLevel.PARTNER,
                query_data_class=UserGetExternalService)
    def getFromDiscord(self, request: ApiRequest, query: UserGetExternalService):
        try:
            user_ext_service: UserExternalService = UserExternalService.get_from_service_account_id(
                ExtServicesCode.DISCORD, query.service_account_id)
        except RuntimeError:
            raise ApiDefaultError(comment="User ext service not found", error_type=ErrorType.NOT_FOUND)
        if request.application.access_level.value < ApiAccessLevel.PRIVATE.value:
            if user_ext_service.visible is False:
                raise ApiDefaultError(comment="User ext service not found", error_type=ErrorType.NOT_FOUND)

        return ApiMethodResult(response=user_ext_service.user.data_model.dict(),
                               request_type=RequestType.POST)

    @api_method(request_methods=[RequestType.POST],
                access_level=ApiAccessLevel.PARTNER,
                query_data_class=UserGetExternalService)
    def getFromVk(self, request: ApiRequest, query: UserGetExternalService):
        try:
            user_ext_service: UserExternalService = UserExternalService.get_from_service_account_id(
                ExtServicesCode.VK, query.service_account_id)
        except RuntimeError:
            raise ApiDefaultError(comment="User ext service not found", error_type=ErrorType.NOT_FOUND)

        if request.application.access_level.value < ApiAccessLevel.PRIVATE.value:
            if user_ext_service.visible is False:
                raise ApiDefaultError(comment="User ext service not found", error_type=ErrorType.NOT_FOUND)

        return ApiMethodResult(response=user_ext_service.user.data_model.dict(),
                               request_type=RequestType.POST)
