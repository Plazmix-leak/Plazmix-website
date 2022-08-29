from flask import render_template

from app.core.permissions import rule_access_check
from app.core.permissions.permissions import Permissions
from app.helper.decorators.web import login_required
from app.helper.online import OnlineCollections, ModeCollection
from app.helper.online.mode import ServerOnlineNode
from app.lib.bukkit.info import BukkitServerInfo
from app.lib.clarence.metric import Metric
from ... import panel


@panel.route('/')
@panel.route('/main')
@login_required
@rule_access_check(Permissions.PANEL_ACCESS)
def main():
    server_information = BukkitServerInfo()
    total_online: ServerOnlineNode = OnlineCollections.get_from_type(ModeCollection.TOTAL).value
    # todo перенести на Ajax
    return render_template('adminpanel/elements/main/main.html', server_information=server_information,
                           current_online=total_online.get_current_online(),
                           online_peak=total_online.get_current_online(),
                           today_peak=total_online.get_clarence().today().max,
                           api_sum=Metric("api").today().sum)
