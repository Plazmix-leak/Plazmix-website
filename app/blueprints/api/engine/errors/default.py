from flask import jsonify

from app.blueprints.api.engine.types.error_code import ErrorType


class ApiDefaultError(Exception):
    def __init__(self, comment, error_type: ErrorType):
        self.comment = comment
        self.error_type = error_type

    def generate_request(self):
        body = {"comment": self.comment,
                "name": self.error_type.name}
        return jsonify(body), self.error_type.value
