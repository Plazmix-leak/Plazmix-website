from functools import wraps

from flask import url_for

from app.core.store import StoreProduct
from app.helper.simple_page import ErrorPage, PageButton, ButtonType


def product_valid(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        error = ErrorPage(comment="Товар не найден!").add_button(
            PageButton(url=url_for('.index'), text="Вернуться в магазин", button_type=ButtonType.COLOR_PRIMARY)
        )
        product_id = kwargs.get('product_id', None)
        if product_id is None:
            return error.build()

        try:
            product: StoreProduct = StoreProduct.get_from_id(product_id)
        except ValueError:
            return error.build()

        if product.active is False:
            return error.build()

        kwargs["product"] = product
        return function(*args, **kwargs)

    return wrapper
