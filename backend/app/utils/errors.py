import logging
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from app.extensions import db

logger = logging.getLogger(__name__)


def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({
            "success": False,
            "message": "Validation failed.",
            "errors": e.messages
        }), 422

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e):
        db.session.rollback()
        logger.exception("Database integrity error")
        return jsonify({
            "success": False,
            "message": "A database conflict occurred. This record may already exist.",
            "errors": {}
        }), 409

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            "success": False,
            "message": "The requested resource was not found.",
            "errors": {}
        }), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({
            "success": False,
            "message": "Method not allowed.",
            "errors": {}
        }), 405

    @app.errorhandler(500)
    def handle_internal_error(e):
        db.session.rollback()
        logger.exception("Unhandled internal server error")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred. Please try again later.",
            "errors": {}
        }), 500