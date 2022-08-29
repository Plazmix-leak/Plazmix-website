from app.blueprints.api.engine.errors.default import ApiDefaultError
from app.blueprints.api.engine.errors.unknown import UnknownMethodOrClassError
from app.blueprints.api.engine.request import ApiRequest
from app.blueprints.api.engine.types.error_code import ErrorType
from app.blueprints.api.engine.version.version import ApiVersion
from app.lib.clarence.counter import MetricCounter


class ApiCore:
    def __init__(self):
        self._version_collection: dict[str, ApiVersion] = {}

    def register_version(self, version: ApiVersion):
        self._version_collection[version.version_name] = version

    def run(self, version_name, method_signature):
        MetricCounter("api_requests").add_count(1)
        try:
            version: ApiVersion = self._version_collection.get(version_name, None)
            if version is None:
                raise UnknownMethodOrClassError()

            request = ApiRequest.generate(method_signature)

            if request.application.can_use() is False:
                raise ApiDefaultError(comment="Unfortunately, our API has restrictions"
                                              " on both methods and applications of the developer."
                                              " You have exceeded the request limit for your developer app."
                                              " According to our policy, zeroing will take place in 24 hours"
                                              " from the moment of your first request for this application,"
                                              " if you need to increase quotas, then contact us -"
                                              " https://vk.me/plazmixdevs Important, your software will"
                                              " have to pass our verification, after which we can increase"
                                              " the daily request limit. All requests of this type are considered"
                                              " on an individual basis by the project administration."
                                              " Thank you for understanding",
                                      error_type=ErrorType.FORBIDDEN)

            res = version(request=request)
            request.application.new_use()
            return res

        except ApiDefaultError as ae:
            return ae.generate_request()
