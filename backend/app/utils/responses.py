import logging
from flask import jsonify

logger = logging.getLogger(__name__)


def success_response(data, message, status_code=200):
    return jsonify({"success": True, "data": data, "message": message}), status_code


def error_response(message, errors=None, status_code=400):
    return jsonify({"success": False, "message": message, "errors": errors or {}}), status_code