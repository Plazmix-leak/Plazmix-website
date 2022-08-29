from .error import EventError


class EventListener:
    def post(self):
        raise EventError("Is method not implemented in this listener")

    def get(self):
        raise EventError("Is method not implemented in this listener")

    def __repr__(self):
        return self.__class__.__name__

    __str__ = __repr__
