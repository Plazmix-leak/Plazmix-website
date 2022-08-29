from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.types.error_code import ErrorType


class ApiCoreError(ApiDefaultError):
    def __init__(self):
        super(ApiCoreError, self).__init__(comment="The error occurred during the processing of your request,"
                                                   " please read the documentation and try again,"
                                                   " if the error persists,"
                                                   " then contact us - https://vk.me/plazmixdevs",
                                           error_type=ErrorType.BAD_SYNTAX)
