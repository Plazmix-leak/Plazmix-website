from enum import Enum


class LinkOwnerType(Enum):
    PLAZMIX = 'plzmx'
    BOT = "bot"
    SYSTEM = "system"


class RedirectType(Enum):
    DEFAULT = "default"
    SPEED = "speed"
