from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.types.error_code import ErrorType


class PermissionDenied(ApiDefaultError):
    def __init__(self):
        super(PermissionDenied, self).__init__(comment="The rights of your application are not sufficient to"
                                                       " receive this content, if you think that this is an error,"
                                                       " please contact us - https://vk.me/plazmixdevs",
                                               error_type=ErrorType.FORBIDDEN)
