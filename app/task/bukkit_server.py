import os

from mcipc.rcon.je import Client

from app import celery
from app.core.permissions.groups import PermissionGroups
from app.core.user import User
from app.helper.online import OnlineCounterHelper
from app.lib.cloudnet.wrapper import CloudNetApiWrapper


def __server_command(command, *args):
    with Client(host=os.getenv('RCON_HOST'), port=int(os.getenv('RCON_PORT')), passwd=os.getenv('RCON_PASSWORD'),
                timeout=10) as client:
        return client.run(command, *args)


@celery.task(name="bukkit.give_group", bind=True, max_retries=5)
def give_group(self, user_uuid: str, group):
    try:
        user: User = User.get_from_uuid(uuid=user_uuid)
    except ValueError:
        return "Unknown user"
    already_group = user.all_permission_group
    new_group = PermissionGroups.get_from_technical_name(group).value
    already_group.append(new_group)
    permission_db_list = " ".join(str(group.get_technical_name) for group in already_group)
    user.bukkit.update_permission_groups(permission_db_list)
    return "Ok"


@celery.task(name="bukkit.remove_group", bind=True, max_retries=5)
def remove_group(self, user_uuid: str, group):
    try:
        user: User = User.get_from_uuid(uuid=user_uuid)
    except ValueError:
        return "Unknown user"
    already_group = user.all_permission_group
    rv_group = PermissionGroups.get_from_technical_name(group).value
    already_group.remove(rv_group)
    permission_db_list = " ".join(str(group.get_technical_name) for group in already_group)
    user.bukkit.update_permission_groups(permission_db_list)
    return "Ok"


@celery.task(name="bukkit.banned_user")
def banned_user(user_uuid: str):
    try:
        user: User = User.get_from_uuid(uuid=user_uuid)
    except ValueError:
        return "Unknown user"
    __server_command("ban", user.bukkit.nickname, "e", "Подробнее на Plazmix.net")
    return "Ok"


@celery.task(name="bukkit.unban_user")
def unban_user(user_uuid: str):
    try:
        user: User = User.get_from_uuid(uuid=user_uuid)
    except ValueError:
        return "Unknown user"

    __server_command("unban", user.bukkit.nickname)
    return "Ok"


@celery.task(name="bukkit.update_online")
def update_online():
    helper = OnlineCounterHelper()
    cloud_net = CloudNetApiWrapper(os.getenv('CLOUD_NET_USER'),
                                   os.getenv('CLOUD_NET_PWD'),
                                   os.getenv('CLOUD_NET_REST'))
    try:
        service_information = cloud_net.fetch_services()
    except RuntimeError:
        helper.save_result()
        return "Fail request, but online update success"

    for service in service_information:
        properties: dict = service.get("properties", {})
        configuration: dict = service.get("configuration", {})
        service_id: dict = configuration.get("serviceId", {})
        online_state = properties.get("Online", False)
        players = properties.get("Online-Count", 0)
        service_name = service_id.get("taskName", "unknown")
        if online_state is False:
            continue
        try:
            helper.add(service_name, players)
        except RuntimeError:
            print(f"Service {service_name} is unknown. Online: {players}")

    helper.save_result()
    return "Ok"
