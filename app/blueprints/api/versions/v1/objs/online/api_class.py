from abc import ABC

from app.blueprints.api.engine.api_class.interface import IApiClass
from app.blueprints.api.engine.api_class.method.decorator import api_method
from app.blueprints.api.engine.api_class.method.result import ApiMethodResult
from app.blueprints.api.engine.api_class.settings import ApiClassSettings
from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.request import ApiRequest
from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel
from app.blueprints.api.engine.types.error_code import ErrorType
from app.blueprints.api.engine.types.request import RequestType
from app.blueprints.api.versions.v1.objs.online.data_class.request import NodeInformation
from app.helper.online import OnlineCollections, OnlineNodesCollection
from app.helper.online.data import ServerOnlineResultDataCls


class Online(IApiClass, ABC):
    def settings(self) -> ApiClassSettings:
        return ApiClassSettings(access_level=ApiAccessLevel.DEFAULT)

    @api_method(request_methods=[RequestType.GET])
    def now(self, request: ApiRequest, query):
        summary = [element.value.get_data_cls() for element in OnlineCollections]
        nodes = [node.value.get_data_cls() for node in OnlineNodesCollection]
        online = ServerOnlineResultDataCls(summary=summary, modes=nodes)
        return ApiMethodResult(request_type=RequestType.GET,
                               response=online.dict())

    @api_method(request_methods=[RequestType.POST], query_data_class=NodeInformation)
    def getFromIdentification(self, request: ApiRequest, query: NodeInformation):
        if "summary" in query.identification:
            try:
                node = OnlineCollections.get_from_name(query.identification)
            except ValueError:
                raise ApiDefaultError(comment="Unknown summary", error_type=ErrorType.BAD_SYNTAX)
        else:
            try:
                node = OnlineNodesCollection.get_from_name(query.identification)
            except ValueError:
                raise ApiDefaultError(comment="Unknown summary", error_type=ErrorType.BAD_SYNTAX)
        return ApiMethodResult(request_type=RequestType.POST,
                               response=node.value.get_data_cls().dict())







