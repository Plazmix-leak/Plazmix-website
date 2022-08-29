from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.types.error_code import ErrorType
from app.blueprints.api.helpers.paginate.data_class import PaginateDataClass
from app.blueprints.api.helpers.paginate.response import PaginationResponse


def get_from_paginate(model, paginate_dc: PaginateDataClass, page_limit=50) -> tuple[list, PaginationResponse]:
    if paginate_dc.count_per_page > page_limit:
        raise ApiDefaultError(comment=f"You have exceeded the"
                                      f" limit for the page, the limit for"
                                      f" this method is - {page_limit}", error_type=ErrorType.BAD_SYNTAX)
    res = model.query.order_by(model.id.desc()).paginate(paginate_dc.page,
                                                         max_per_page=paginate_dc.count_per_page,
                                                         error_out=False)
    elements = res.items
    pagination_response = PaginationResponse(
        max_page=res.pages,
        current_page=paginate_dc.page,
        items_in_page=len(elements)
    )

    if not res:
        return [], pagination_response

    return [el.data_model for el in elements], pagination_response
