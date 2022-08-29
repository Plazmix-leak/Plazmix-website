import os

from flask import request

from app.blueprints.event.engine import EventError
from app.blueprints.event.engine.error import EventResponse
from app.blueprints.event.engine.listener import EventListener

GROUP_TO_AUTHOR = {
    201104908: "Plazmix Network",
    201759806: "Build Team",
    199412539: "Development Team",
    197465775: "Staff Team"
}


class VkListener(EventListener):
    def post(self):
        raw_data: dict = request.get_json(force=True)

        if raw_data.get('type') == "confirmation":
            raise EventResponse(os.getenv('EVENT_VK_CONFIRMATION'))

        if raw_data.get('type') != "wall_post_new":
            raise EventError("Unsupported event type")

        author_id = raw_data.get("group_id", 0)
        author = GROUP_TO_AUTHOR.get(author_id, None)

        if author is None:
            raise EventError("Unknown author")
        # Generate vk append event
        from app.task.tools import vk_event_post_generate
        vk_event_post_generate.apply_async(
            kwargs={"raw_data": raw_data,
                    "author": author},
            ignore_result=True)

        raise EventResponse("Ok")




