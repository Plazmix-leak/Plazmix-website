from abc import ABC, abstractmethod

from flask import render_template


class AbstractStoreProduct(ABC):
    def __init__(self, *, technical_name, name, html, image, price, sale_percent=0):
        self._technical_name = technical_name
        self._name = name
        self._html = html
        self._price = price
        self._image = image
        self._sale_percent = sale_percent

    @property
    def have_active_sale(self) -> bool:
        if self._sale_percent == 0:
            return False
        return True

    @property
    def action_size(self) -> int:
        return self._sale_percent

    @property
    def image(self):
        return self._image

    @property
    def raw_price(self):
        return self._price

    @property
    def price(self):
        if self.have_active_sale:
            return int((1 - (self.action_size/100)) * self._price)
        return self._price

    @property
    def name(self):
        return self._name

    @property
    def technical_name(self):
        return self._technical_name

    @property
    def html(self):
        if 'html' not in self._html:
            return self._html
        return render_template(f"application/store/product/{self.__class__.__name__}/{self._html}")

    @abstractmethod
    def give(self, user):
        pass
