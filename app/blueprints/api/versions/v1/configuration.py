from app.blueprints.api.engine.version import ApiVersion

from .objs import *


class PublicV1ApiConfiguration(ApiVersion):
    def __init__(self):
        super(PublicV1ApiConfiguration, self).__init__("v1")

        self.register_methods(Online)
        self.register_methods(News)
        self.register_methods(User)
        self.register_methods(GameUser)
        self.register_methods(ModeratorAlert)
        self.register_methods(Oauth2)
        self.register_methods(Metric)
