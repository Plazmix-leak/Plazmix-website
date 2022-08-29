from app.blueprints.api.engine.version import ApiVersion

from .objs import *


class SiteApiConfiguration(ApiVersion):
    def __init__(self):
        super(SiteApiConfiguration, self).__init__("siteV1")

        self.register_methods(Online)
