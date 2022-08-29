import os

from flask import request, url_for


def get_next_page():
    next_page = request.args.get('next') or url_for('main.index')
    if os.getenv('SERVER_NAME').lower() not in next_page.lower():
        next_page = url_for('main.index')
    return next_page
