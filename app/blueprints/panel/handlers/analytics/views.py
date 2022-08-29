from flask import render_template

from app.core.permissions import Permissions, rule_access_check
from ... import panel


@panel.route('/analytics/api')
@rule_access_check(Permissions.PANEL_ACCESS)
def analytics_api():
    return render_template('adminpanel/elements/analytics/api.html')


@panel.route('/analytics/players')
@rule_access_check(Permissions.PANEL_ACCESS)
def analytics_players():
    return render_template('adminpanel/elements/analytics/players.html')