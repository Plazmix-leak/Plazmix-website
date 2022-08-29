from .data_class import BadgeDataClass


class Badge:
    def __init__(self, name, admin_name, title, icon_class, color):
        self._admin_name = admin_name
        self._technical_name = name
        self._title = title
        self._icon = icon_class
        self._color = color

    def get_title(self, user):
        return self._title.format(user=user)

    def data_class(self, user):
        return BadgeDataClass(technical_name=self.technical_name,
                              description=self.get_title(user))

    @property
    def admin_name(self):
        return self._admin_name

    @property
    def technical_name(self):
        return self._technical_name

    @property
    def icon(self):
        return self._icon

    @property
    def color(self):
        return self._color

    def __eq__(self, other):
        return self.technical_name == other.technical_name
