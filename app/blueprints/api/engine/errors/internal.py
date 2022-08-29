from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.types.error_code import ErrorType


class InternalApiError(ApiDefaultError):
    def __init__(self):
        super(InternalApiError, self).__init__(comment="You have stumbled upon an internal server error,"
                                                       " please contact us - https://vk.me/plazmixdevs",
                                               error_type=ErrorType.INTERNAL_ERROR)
