from flask import render_template

from .. import store
from ..engine.collection.imp.groups import GroupStoreCollection


@store.route('/')
def index():
    return render_template('application/store/index.html', products=GroupStoreCollection)