from .._config import ShortLinkConfig
from ._request_engine import ShortLinkEngine
from .._data_model import LinkDataModel
from ..error import LinkDoesNotExist
from .icore import ICore


class ShortLinkBaseCore(ICore):
    def __init__(self):
        self.__engine = ShortLinkEngine(endpoint=ShortLinkConfig.ENDPOINT,
                                        api_token=ShortLinkConfig.API_TOKEN, api_version="v1")

    def link_control(self, http_method, link):
        method = f'link/{link.id}'
        if http_method == "get":
            result = self.__engine(method, http_method='get')
            return LinkDataModel.parse_obj(result.get('result', {}))
        elif http_method == "delete":
            result = self.__engine(method, http_method='delete')
            if result.get('result', "no") == 'ok':
                return True
            raise LinkDoesNotExist()
        elif http_method == "put":
            result = self.__engine(method, http_method='put', body=link.data_model.dict())
            return LinkDataModel.parse_obj(result.get('result', {}))
        else:
            raise ValueError("unknown http method")

    def get_all_owner_link(self, owner_id: str):
        result = self.__engine(f'owner/{owner_id}', http_method='get')
        return [(LinkDataModel.parse_obj(current_data), self) for current_data in result]

    def create_new_link(self, owner_id: str, real_link: str, redirect_type: str, uri=None, disposable=False):
        model = LinkDataModel(owner_id=owner_id, real_link=real_link, uri=uri,
                              disposable=disposable, redirect_type=redirect_type)
        result = self.__engine('link/create', model.dict())
        return LinkDataModel.parse_obj(result.get('result', {})), self

    def get_link_from_id(self, link_id: int):
        result = self.__engine(f'link/{link_id}', http_method='get')
        return LinkDataModel.parse_obj(result.get('result', {})), self

    def get_link_from_uri(self, uri: str):
        result = self.__engine(f'link/uri/{uri}', http_method='get')
        return LinkDataModel.parse_obj(result.get('result', {})), self
