class GiftError(Exception):
    pass


class GiftIsNotActiveError(GiftError):
    pass


class GiftNotFound(GiftError):
    pass


class GiftActivateError(GiftError):
    pass
