from flask import Blueprint
from .engine.core import ApiCore

api_core = ApiCore()
api = Blueprint('api', __name__)

from .register import *
from .handlers import *
