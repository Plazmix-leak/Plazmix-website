from flask import render_template

from app.helper.simple_page.simple import SimplePage
from app.helper.template import get_random_background


class GrayPage(SimplePage):
    def __init__(self, title="Инфо", comment="Инфо",
                 page_title="Инфо", form=None):
        super(GrayPage, self).__init__(title=title, comment=comment, page_title=page_title,
                                       form=form, icon=None, icon_color=None)

    def build(self):
        return render_template('helpers/simple_page/gray.html', simple_page=self,
                               background=get_random_background())
