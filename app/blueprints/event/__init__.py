from flask import Blueprint

events = Blueprint('events', __name__)

from .handler import *
