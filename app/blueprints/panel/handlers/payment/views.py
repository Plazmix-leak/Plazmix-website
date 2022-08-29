from flask import render_template

from app.core.permissions import Permissions, rule_access_check
from app.helper.decorators.web import login_required
from ... import panel


@panel.route('/payment/history')
@login_required
@rule_access_check(Permissions.ADMIN_ACCESS)
def payment_history():
    return render_template('adminpanel/elements/payment/list.html')