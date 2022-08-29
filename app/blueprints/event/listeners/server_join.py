from flask import request

from app.blueprints.event.engine.error import EventResponse
from app.blueprints.event.engine.listener import EventListener


class ServerJoin(EventListener):
    def get(self):
        key = request.args.get("key")
        user_ip = request.args.get("user_ip")
        user_uuid = request.args.get("user_uuid")

        # Create task
        from app.task.tools import event_server_join
        event_server_join.apply_async(
            kwargs={"key": key,
                    "user_uuid": user_uuid,
                    "user_ip": user_ip},
            ignore_result=True)

        raise EventResponse("Ok")
