from flask import render_template

from app.helper.simple_page.simple import SimplePage


class AdminPanelSimplePage(SimplePage):
    def __init__(self, title="Инфо", comment="Инфо",
                 page_title="Инфо", form=None):
        super(AdminPanelSimplePage, self).__init__(title=title, comment=comment, page_title=page_title,
                                                   form=form, icon=None, icon_color=None)

    def build(self):
        return render_template('helpers/simple_page/adminpanel/simple.html', simple_page=self)


class AdminPanelErrorPage(AdminPanelSimplePage):
    def __init__(self, comment="Ошибка"):
        super(AdminPanelErrorPage, self).__init__(title="Ошибка", comment=comment, page_title="Ошибка",
                                                  form=None)
