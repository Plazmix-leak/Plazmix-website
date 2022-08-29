from flask import request

from app.blueprints.event.engine.error import EventResponse
from app.blueprints.event.engine.listener import EventListener


class ServerUserEditGroup(EventListener):
    def get(self):
        key = request.args.get("key")
        user_uuid = request.args.get("user_uuid")

        # Create task
        from app.task.tools import event_user_edit_group
        event_user_edit_group.apply_async(
            kwargs={"key": key,
                    "user_uuid": user_uuid},
            ignore_result=True)

        raise EventResponse("Ok")
