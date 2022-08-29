from flask import render_template

from app.core.permissions import Permissions, rule_access_check
from app.helper.decorators.web import login_required
from ... import panel


@panel.route('/staff/list')
@login_required
@rule_access_check(Permissions.PANEL_ACCESS)
def staff_list():
    return render_template('adminpanel/elements/staff/list.html')


@panel.route('/staff/list/<cluster>')
@login_required
@rule_access_check(Permissions.PANEL_ACCESS)
def staff_list_cluster(cluster):
    return render_template('adminpanel/elements/staff/list_cluster.html', cluster=cluster)
