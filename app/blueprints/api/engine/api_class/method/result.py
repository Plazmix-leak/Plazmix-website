import json

from app.blueprints.api.engine.types.request import RequestType


class ApiMethodResult:
    def __init__(self, request_type: RequestType, response):
        self.request_type = request_type
        self.response = response

    def get_response(self):
        return json.dumps(self.response)
