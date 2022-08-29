from flask import url_for, abort, render_template, request, flash, g
from werkzeug.utils import redirect

from app.core.user import User
from app.core.permissions.groups import PermissionGroups
from app.helper.decorators.web import login_required
from app.helper.flash_types import FlashTypes
from .. import profile


@profile.route('/')
@profile.route('/@<user_nickname>')
@profile.route('/u/<user_uuid>')
def user_profile(user_uuid=None, user_nickname=None):
    if user_uuid is not None:
        try:
            profile_user: User = User.get_from_uuid(user_uuid)
        except ValueError:
            return abort(404)
    elif user_nickname is not None:
        try:
            profile_user: User = User.get_from_nickname(user_nickname)
        except ValueError:
            return abort(404)
    else:
        if g.user is None:
            return redirect(url_for('main.index'))

        profile_user: User = g.user

    return render_template('application/profile/profile.html', profile=profile_user)


@profile.route('/search')
@login_required
def search():
    def add_default(array):
        array += User.get_all_user_from_group(PermissionGroups.OWN)
        array += User.get_all_user_from_group(PermissionGroups.ADMINISTRATOR)
        array += User.get_all_user_from_group(PermissionGroups.MODERATOR_PLUS)

    def build_page(result_profiles, q):
        return render_template('application/profile/search.html', result_profiles=result_profiles, q=q)

    search_argument = request.args.get("q", None)
    result = []

    if search_argument is None:
        add_default(result)
        return build_page(result, search_argument)
    if len(search_argument) < 3:
        flash("Поисковый запрос не может быть менее 3-х символов", FlashTypes.ERROR)
        add_default(result)
        return build_page(result, search_argument)

    result += sorted(User.search_from_nickname(search_argument),
                     key=lambda element: element.permission_group, reverse=True)

    return build_page(result, search_argument)
