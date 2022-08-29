from typing import List

from flask import render_template
from .button import PageButton
from ..template import get_random_background


class SimplePage:
    def __init__(self, title="Инфо", comment="Инфо",
                 page_title="Инфо",
                 icon="fad fa-globe fa-7x", icon_color="#2940bb", form=None):
        self.title = title
        self.comment = comment
        self.icon = icon
        self.page_title = page_title
        self.icon_color = icon_color
        self._form = form

        self._buttons = []

    @property
    def form(self):
        return self._form

    @property
    def buttons(self) -> List[PageButton]:
        return self._buttons

    def add_button(self, button: PageButton):
        self._buttons.append(button)
        return self

    def clear_buttons(self):
        self._buttons.clear()
        return self

    def set_form(self, form):
        self._form = form
        return self

    def build(self):
        return render_template('helpers/simple_page/background.html',
                               simple_page=self, background=get_random_background())
