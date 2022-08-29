from app.blueprints.api.engine.version import ApiVersion

from .objs import *


class AdminPanelApiConfiguration(ApiVersion):
    def __init__(self):
        super(AdminPanelApiConfiguration, self).__init__("adminPanel")

        self.register_methods(Online)
        self.register_methods(Balance)
        self.register_methods(Logs)
        self.register_methods(Staff)
        self.register_methods(Metric)
        self.register_methods(PaymentHistory)
        self.register_methods(Forms)
