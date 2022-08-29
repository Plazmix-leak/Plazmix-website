from flask import Blueprint

dev = Blueprint('developers', __name__)

from .handler import *