from flask import Blueprint

panel = Blueprint('panel', __name__)

from .handlers import *