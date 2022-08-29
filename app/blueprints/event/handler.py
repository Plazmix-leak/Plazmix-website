from . import events
from .main import event_engine


@events.route('/listener/<event_cls_name>', methods=['GET', 'POST'])
def event_handler(event_cls_name):
    return event_engine.run(event_cls_name)


@events.errorhandler(404)
def event_404():
    return "Listener not found"
