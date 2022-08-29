from flask import Blueprint

gift = Blueprint('gift', __name__)

from .handler import *