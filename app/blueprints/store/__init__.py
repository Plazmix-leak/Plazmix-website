from flask import Blueprint

store = Blueprint('store', __name__)

from .handlers.main import *
from .handlers.buy import *