from flask import jsonify
from sentry_sdk import capture_exception

from . import api, api_core


@api.route("/<api_version>/<api_cls>.<api_func>", methods=["GET", "POST"])
def api_handler(api_version: str, api_cls: str, api_func: str):
    api_method = f"{api_cls}.{api_func}"
    return api_core.run(version_name=api_version, method_signature=api_method)


@api.errorhandler(404)
def api_error_404(*args, **kwargs):
    return jsonify({
        "name": "SYSTEM_NOT_FOUND",
        "comment": "Hmm, it looks like you've hit a black hole. It seems that you need to read the documentation"
    }), 404


@api.errorhandler(500)
def api_error_500(error):
    capture_exception(error)
    return jsonify({"comment": "Oops! This error can not be processed validly,"
                               " please contact us - https://vk.me/plazmixdevs",
                    "name": "SYSTEM_INTERNAL_ERROR"}), 500

