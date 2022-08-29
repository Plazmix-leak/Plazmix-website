from .engine.engine import EventEngine
from .listeners.enot_pay import EnotPayHandler
from .listeners.vk import VkListener
from .listeners.server_join import ServerJoin
from .listeners.server_user_edit_group import ServerUserEditGroup

event_engine = EventEngine()

event_engine.add_listener(VkListener)
event_engine.add_listener(ServerJoin)
event_engine.add_listener(ServerUserEditGroup)
event_engine.add_listener(EnotPayHandler)
