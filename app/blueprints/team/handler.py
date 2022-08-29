from flask import render_template, abort, request

from . import team
from app.helper.decorators.web import login_required
from app.core.form.engine import FormEngine
from app.core.user import User
from app.core.permissions.groups import PermissionGroups, STAFF_GROUPS

_ALLOWED_GROUPS = sorted(STAFF_GROUPS, key=lambda x: x.value, reverse=True)


@team.route('/')
def index():
    return render_template('application/team/index.html')


@team.route('/list')
def staff_list():
    return render_template('application/team/staff_list.html', groups=_ALLOWED_GROUPS)


@team.route('/form/<technical_name>', methods=['GET', 'POST'])
@login_required
def form(technical_name):
    try:
        form_base = FormEngine.get_from_technical_name(technical_name)
    except ValueError:
        return abort(404)
    return form_base.page()


@team.route('/ajax/users_in_group')
def get_users_in_group():
    user_group_raw = request.args.get('group', None)
    if user_group_raw is None:
        return "None"

    user_group = PermissionGroups.get_from_technical_name(user_group_raw)

    check = False
    for ag in _ALLOWED_GROUPS:
        if user_group.value == ag.value:
            check = True
            break

    if check is False:
        return "None"

    users = User.get_all_user_from_group(user_group)
    if not users:
        return "None"
    return render_template("application/team/ajax/userss_in_group.html", users=users)
