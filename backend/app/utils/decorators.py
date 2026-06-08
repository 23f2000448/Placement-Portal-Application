from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def _make_error(message, status_code):
    return jsonify({"success": False, "message": message, "errors": {}}), status_code

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "admin":
            return _make_error("Admin access required.", 403)
        return fn(*args, **kwargs)
    return wrapper

def company_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "company":
            return _make_error("Company access required.", 403)
        return fn(*args, **kwargs)
    return wrapper

def student_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "student":
            return _make_error("Student access required.", 403)
        return fn(*args, **kwargs)
    return wrapper

def approved_company_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "company":
            return _make_error("Company access required.", 403)
        if not claims.get("is_approved"):
            return _make_error("Your company profile is not yet approved by admin.", 403)
        return fn(*args, **kwargs)
    return wrapper