from .button_type import ButtonType


class PageButton:
    def __init__(self, url, text, button_type=ButtonType.COLOR_INFO):
        self.url = url
        self.text = text
        self.style_class = button_type
