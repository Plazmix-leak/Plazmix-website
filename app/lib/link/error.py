class LinkDefaultError(Exception):
    pass


class LinkDoesNotExist(LinkDefaultError):
    pass


class LinkServerError(LinkDefaultError):
    pass
