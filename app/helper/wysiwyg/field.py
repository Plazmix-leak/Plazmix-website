from wtforms.fields import Field

from .widget import WysiwygWidget


class WysiwygField(Field):
    widget = WysiwygWidget()

    def __init__(self, label='', validators=None, **kwargs):
        super(WysiwygField, self).__init__(label, validators, **kwargs)
