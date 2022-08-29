from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.types.error_code import ErrorType


class UnknownMethodOrClassError(ApiDefaultError):
    def __init__(self):
        super(UnknownMethodOrClassError, self).__init__(comment="There is no such api class or version,"
                                                                " please read the documentation and try again,"
                                                                " if you think that this method or api version"
                                                                " should exist, then contact us"
                                                                " - https://vk.me/plazmixdevs",
                                                        error_type=ErrorType.BAD_SYNTAX)
