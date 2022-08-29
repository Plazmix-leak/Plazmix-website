from .groups import MODERATION_GROUPS


def check_moderator(user):

    user_groups = user.all_permission_group
    check = False
    for group in user_groups:
        for mg in MODERATION_GROUPS:
            if group == mg.value:
                check = True
                break
    return check
