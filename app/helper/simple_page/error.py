from .simple import SimplePage


class ErrorPage(SimplePage):
    def __init__(self, title="Ошибка", comment="Ошибка",
                 page_title="Ошибка",
                 icon="fad fa-exclamation-circle fa-7x", icon_color="red"):
        super(ErrorPage, self).__init__(title=title, comment=comment, page_title=page_title,
                                        icon=icon, icon_color=icon_color)
