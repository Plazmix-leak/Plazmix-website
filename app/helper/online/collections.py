from enum import Enum

from .enums import ModeCollection
from .mode import ServerOnlineNode


class _NodeEnum(Enum):
    @classmethod
    def get_from_type(cls, identification):
        for element in cls:
            if element.value.get_technical_name() == identification.value:
                return element
        raise ValueError("Unknown server online node type")

    @classmethod
    def get_from_name(cls, name: str):
        for element in cls:
            if element.value.get_technical_name() == name:
                return element
        raise ValueError("Unknown server online node name")


class OnlineCollections(_NodeEnum):
    total = ServerOnlineNode(ModeCollection.TOTAL.value, "Онлайн проекта")
    project_hub = ServerOnlineNode(ModeCollection.HUB.value, "Хаб проекта")
    lobby = ServerOnlineNode(ModeCollection.LOBBY.value, "Лобби")
    game = ServerOnlineNode(ModeCollection.GAME_SERVER.value, "Игровые сервера")
    technical = ServerOnlineNode(ModeCollection.TECHNICAL.value, "Технические сервера")
    sky_wars = ServerOnlineNode(ModeCollection.SKY_WARS.value, "Мини-игра: SkyWars")
    bed_wars = ServerOnlineNode(ModeCollection.BED_WARS_TOTAL.value, "Мини-игра: BedWars")
    bed_wars_classic = ServerOnlineNode(ModeCollection.BED_WARS_CLASSIC.value, "BedWars: Классический")
    bed_wars_points = ServerOnlineNode(ModeCollection.BED_WARS_POINTS.value, "BedWars: Points")

    halloween_simulator = ServerOnlineNode(ModeCollection.HALLOWEEN_SIMULATOR.value, "Halloween Simulator")


class OnlineNodesCollection(_NodeEnum):
    auth = ServerOnlineNode("auth", "Авторизация", collections=[ModeCollection.TECHNICAL])

    main_lobby = ServerOnlineNode("hub", "Хаб", collections=[ModeCollection.HUB])

    bw_lobby = ServerOnlineNode("bwlobby", "Лобби BedWars", collections=[ModeCollection.LOBBY,
                                                                         ModeCollection.BED_WARS_TOTAL])

    sw_lobby = ServerOnlineNode("swlobby", "Лобби SkyWars", collections=[ModeCollection.LOBBY,
                                                                         ModeCollection.SKY_WARS])

    hnlobby = ServerOnlineNode("hnlobby", "Лобби Halloween Simulator", collections=[ModeCollection.HALLOWEEN_SIMULATOR,
                                                                                    ModeCollection.LOBBY])

    events = ServerOnlineNode("eventserver", "Сервер для ивентов", collections=[ModeCollection.TECHNICAL,
                                                                                ModeCollection.GAME_SERVER])

    # SkyWars
    sws = ServerOnlineNode("sws", "SkyWars Solo (Insane)", collections=[ModeCollection.GAME_SERVER,
                                                                        ModeCollection.SKY_WARS])

    # swr = ServerOnlineNode("rsw", "SkyWars ранкед", collections=[ModeCollection.GAME_SERVER,
    #                                                              ModeCollection.SKY_WARS])

    swd = ServerOnlineNode("swd", "SkyWars командный", collections=[ModeCollection.GAME_SERVER,
                                                                    ModeCollection.SKY_WARS])

    # BedWars classic
    bws = ServerOnlineNode("bws", "BedWars 2X8", collections=[ModeCollection.GAME_SERVER,
                                                              ModeCollection.BED_WARS_TOTAL,
                                                              ModeCollection.BED_WARS_CLASSIC])

    bwd = ServerOnlineNode("bwd", "BedWars 3X4", collections=[ModeCollection.GAME_SERVER,
                                                              ModeCollection.BED_WARS_TOTAL,
                                                              ModeCollection.BED_WARS_CLASSIC])

    bwq = ServerOnlineNode("bwq", "BedWars 4X4", collections=[ModeCollection.GAME_SERVER,
                                                              ModeCollection.BED_WARS_TOTAL,
                                                              ModeCollection.BED_WARS_CLASSIC])

    # BedWars points
    bwsp = ServerOnlineNode("bwsp", "BedWars Points 2X8", collections=[ModeCollection.GAME_SERVER,
                                                                       ModeCollection.BED_WARS_TOTAL,
                                                                       ModeCollection.BED_WARS_POINTS])

    bwdp = ServerOnlineNode("bwdp", "BedWars Points 3X4", collections=[ModeCollection.GAME_SERVER,
                                                                       ModeCollection.BED_WARS_TOTAL,
                                                                       ModeCollection.BED_WARS_POINTS])

    bwqp = ServerOnlineNode("bwqp", "BedWars Points 4X4", collections=[ModeCollection.GAME_SERVER,
                                                                       ModeCollection.BED_WARS_TOTAL,
                                                                       ModeCollection.BED_WARS_POINTS])

    hwg = ServerOnlineNode("hwg", "Halloween Simulator", collections=[ModeCollection.HALLOWEEN_SIMULATOR,
                                                                      ModeCollection.GAME_SERVER])
