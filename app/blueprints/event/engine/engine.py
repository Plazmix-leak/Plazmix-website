from flask import request, jsonify
from sentry_sdk import capture_exception

from app.blueprints.event.engine.error import EventError, EventResponse
from app.blueprints.event.engine.listener import EventListener


class EventEngine:
    def __init__(self):
        self._listeners = {}

    def add_listener(self, listener_cls):
        if issubclass(listener_cls, EventListener) is False:
            raise RuntimeError("is not sub class")
        self._listeners[listener_cls.__name__] = listener_cls()

    def run(self, cls_name):
        cls = self._listeners.get(cls_name, None)
        try:
            if cls is None:
                raise EventError("Listener not found")

            request_methods = request.method.lower()
            cls_methods = getattr(cls, request_methods, None)

            if cls_methods is None:
                raise EventError("Unknown http method")

            return jsonify({"response": cls_methods()})

        except EventResponse as response:
            return response.response

        except EventError as event_error:
            capture_exception(event_error)
            return jsonify({
                "error_name": event_error.__class__.__name__,
                "error_cls": cls.__class__.__name__,
                "comment": event_error.comment
            })

        except Exception as ex:
            capture_exception(ex)
            return jsonify({
                "error_name": ex.__class__.__name__,
                "comment": str(ex)
            })

