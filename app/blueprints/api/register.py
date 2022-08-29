from . import api_core
from .versions import *


# Version register

api_core.register_version(SiteApiConfiguration())
api_core.register_version(AdminPanelApiConfiguration())
api_core.register_version(PublicV1ApiConfiguration())





