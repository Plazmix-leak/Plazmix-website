from app.blueprints.api.engine.types.aplication_type import ApiAccessLevel


class ApiClassSettings:
    def __init__(self, access_level: ApiAccessLevel):
        self.access_level = access_level

