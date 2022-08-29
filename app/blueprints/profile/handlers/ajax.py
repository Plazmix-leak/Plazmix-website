from flask import render_template, request

from app.blueprints.gift.engine import UserGift
from app.core.user import User
from .. import profile


@profile.route('/ajax/friends')
def ajax_friends():
    user_uuid = request.args.get('uuid', None)
    if user_uuid is None:
        return "Ошибка!"
    try:
        user = User.get_from_uuid(user_uuid)
    except ValueError:
        return "Ошибка"
    return render_template('application/profile/ajax/friends.html', profile=user)


@profile.route('/ajax/gifts')
def ajax_gifts():
    user_uuid = request.args.get('uuid', None)
    if user_uuid is None:
        return "Ошибка!"
    try:
        user = User.get_from_uuid(user_uuid)
    except ValueError:
        return "Ошибка"
    user_gifts = UserGift.get_all_from_user(user)
    return render_template('application/profile/ajax/gifts.html', gifts=user_gifts)


@profile.route('/ajax/achievements')
def ajax_achievements():
    user_uuid = request.args.get('uuid', None)
    if user_uuid is None:
        return "Ошибка!"
    try:
        user = User.get_from_uuid(user_uuid)
    except ValueError:
        return "Ошибка"
    achievements_list = user.bukkit.achievements
    return render_template('application/profile/ajax/achievements.html', achivements=achievements_list)
