from app.blueprints.api.engine.errors.internal import InternalApiError


class IApiPaginate:
    @property
    def data_model(self):
        raise InternalApiError()