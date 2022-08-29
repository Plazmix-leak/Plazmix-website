from flask import Blueprint

profile = Blueprint('profile', __name__)

from .handlers import *