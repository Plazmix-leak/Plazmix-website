import random

from flask import url_for


def get_random_background():
    image = url_for('static', filename=f"img/background/login/{random.randint(1, 44)}.png")
    return image
