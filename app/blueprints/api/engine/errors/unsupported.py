from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.types.error_code import ErrorType


class UnsupportedError(ApiDefaultError):
    def __init__(self):
        super(UnsupportedError, self).__init__(comment="This method or request type is not supported,"
                                                       " please read the documentation and try again",
                                               error_type=ErrorType.BAD_SYNTAX)
