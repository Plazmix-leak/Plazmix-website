from enum import Enum


class ErrorType(Enum):
    BAD_SYNTAX = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409

    INTERNAL_ERROR = 500
    NOT_IMPLEMENTATION = 501

    USER_NOT_FOUND = 404
