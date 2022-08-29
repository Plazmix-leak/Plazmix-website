import os

from app import celery
from app.blueprints.event.helpers.vk.request import VkWallRequest
from app.core.models.news import News
from app.core.user import User, UserAuthLogs
from app.lib.clarence.counter import MetricCounter


@celery.task(name="tools.event_vk")
def vk_event_post_generate(raw_data, author):
    post = VkWallRequest.parse_obj(raw_data.get('object', {}))

    if not post.text:
        post.text = "Для прочтения полной новости нажмите 'подробнее'"

    if post.post_type.lower() != "post":
        return f"Is not post is {post.post_type}"

    photo = None
    if post.attachments is not None:
        for attachment in post.attachments:
            if attachment.get('type', None) != 'photo':
                continue
            photo_data = attachment.get('photo', {})
            max_width = 0
            for size_data in photo_data.get('sizes', []):
                if size_data.get('width') > max_width:
                    photo = size_data.get('url')
            break

    link = f"https://vk.com/wall{post.owner_id}_{post.id}"
    News.create(text=post.text, author=author, title='Новость с группы ВК', more=link, image=photo)
    return "Post success generate"


@celery.task(name="tools.event_server_join")
def event_server_join(key, user_uuid, user_ip):
    if os.getenv("EVENT_SERVER_KEY") != key:
        return "Invalid api key"

    try:
        user = User.get_from_uuid(user_uuid)
    except ValueError:
        return "Unknown user"

    MetricCounter("server_join").add_count(1)
    UserAuthLogs.create_new(user, "server", user_ip)
    return "Ok"


@celery.task(name="tools.event_user_edit_group")
def event_user_edit_group(key, user_uuid):
    if os.getenv("EVENT_SERVER_KEY") != key:
        return "Invalid api key"

    try:
        user = User.get_from_uuid(user_uuid)
    except ValueError:
        return "Unknown user"

    user.bukkit.clear_cache()
    return "Ok"
