from flask import render_template, g, url_for, redirect

from app.core.user import User
from app.core.panel.models import ModeratorAlert
from app.core.panel.types import ModeratorAlertType
from app.core.permissions import Permissions, rule_access_check
from app.core.permissions.helpers import check_moderator
from app.helper.decorators.web import login_required
from app.helper.simple_page.panel import AdminPanelErrorPage, AdminPanelSimplePage
from .form import NewAlertForm, AlertControlForm
from ... import panel


@panel.route('/moderator/profile')
@panel.route('/moderator/profile/<moderator_uuid>')
@login_required
@rule_access_check(Permissions.PANEL_ACCESS)
def moderation_profile(moderator_uuid=None):
    if moderator_uuid is None:
        moderator: User = g.user
    else:
        moderator = User.get_from_uuid(moderator_uuid)

    if check_moderator(moderator) is False:
        return AdminPanelErrorPage(comment=f"{moderator.bukkit.nickname} не является модератором!").build()

    warnings = ModeratorAlert.get_all_to(to=moderator, alert_type=ModeratorAlertType.WARNING)
    reprimand = ModeratorAlert.get_all_to(to=moderator, alert_type=ModeratorAlertType.REPRIMAND)
    return render_template('adminpanel/elements/moderation/profile.html', moderator=moderator,
                           warnings=warnings, reprimand=reprimand)


@panel.route('/moderator/<moderator_uuid>/new_alert', methods=['POST', 'GET'])
@login_required
@rule_access_check(Permissions.ADD_MODERATOR_ALERT)
def moderation_new_alert(moderator_uuid):
    moderator: User = User.get_from_uuid(moderator_uuid)
    form = NewAlertForm()
    page = AdminPanelSimplePage(title="Выдача варна", page_title="Выдача варна",
                                comment=f"Вы собираетесь выдать варн модератору - {moderator.bukkit.nickname}",
                                form=form)

    if form.validate_on_submit():
        if form.submit.data:
            alert_type = ModeratorAlertType(form.alert_type.data)
            ModeratorAlert.create(g.user, moderator, form.reason.data, alert_type)
        return redirect(url_for('panel.moderation_profile', moderator_uuid=moderator_uuid))
    return page.build()


@panel.route('/moderator/alert/view/<int:alert_id>', methods=['GET', 'POST'])
@login_required
@rule_access_check(Permissions.PANEL_ACCESS)
def moderation_view_alert(alert_id):
    try:
        alert: ModeratorAlert = ModeratorAlert.get_from_id(alert_id)
    except ValueError:
        return AdminPanelErrorPage(comment="Такого варна не существует :(").build()

    form = AlertControlForm()

    if form.validate_on_submit():
        if form.deactivate.data:
            alert.deactivate()
        elif form.activate.data:
            alert.activate()
        elif form.to_moder.data:
            return redirect(url_for('panel.moderation_profile', moderator_uuid=alert.to))

    return render_template('adminpanel/elements/moderation/alert.html', alert=alert, form=form)

