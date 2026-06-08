from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User, UserRole, UserStatus
from app.models.company import Company
from app.models.student import Student
from datetime import datetime, timezone

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def success_response(data, message, status_code=200):
    return jsonify({"success": True, "data": data, "message": message}), status_code


def error_response(message, errors=None, status_code=400):
    return jsonify({"success": False, "message": message, "errors": errors or {}}), status_code



@auth_bp.route("/register/student", methods=["POST"])
def register_student():
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")

    email    = body.get("email", "").strip().lower()
    password = body.get("password", "")
    fullname = body.get("full_name", "").strip()


    errors = {}
    if not email:
        errors["email"] = "Email is required."
    if not password or len(password) < 6:
        errors["password"] = "Password must be at least 6 characters."
    if not fullname:
        errors["full_name"] = "Full name is required."
    if errors:
        return error_response("Validation failed.", errors, 422)

    if User.query.filter_by(email=email).first():
        return error_response("An account with this email already exists.", status_code=409)

    try:
        user = User(email=email, role=UserRole.STUDENT, status=UserStatus.ACTIVE)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        student = Student(user_id=user.id, full_name=fullname)
        db.session.add(student)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response("Registration failed. Please try again.", status_code=500)

    return success_response(
        data={"user_id": user.id, "email": user.email, "role": "student"},
        message="Student registered successfully.",
        status_code=201
    )


@auth_bp.route("/register/company", methods=["POST"])
def register_company():
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")

    email    = body.get("email", "").strip().lower()
    password = body.get("password", "")
    name     = body.get("name", "").strip()


    errors = {}
    if not email:
        errors["email"] = "Email is required."
    if not password or len(password) < 6:
        errors["password"] = "Password must be at least 6 characters."
    if not name:
        errors["name"] = "Company name is required."
    if errors:
        return error_response("Validation failed.", errors, 422)

    if User.query.filter_by(email=email).first():
        return error_response("An account with this email already exists.", status_code=409)


    try:
        user = User(email=email, role=UserRole.COMPANY, status=UserStatus.ACTIVE)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        company = Company(user_id=user.id, name=name)
        db.session.add(company)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response("Registration failed. Please try again.", status_code=500)

    return success_response(
        data={
            "user_id": user.id,
            "email": user.email,
            "role": "company",
            "approval_status": "pending"
        },
        message="Company registered successfully. Await admin approval.",
        status_code=201
    )



@auth_bp.route("/login", methods=["POST"])
def login():
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")

    email    = body.get("email", "").strip().lower()
    password = body.get("password", "")

    if not email or not password:
        return error_response("Email and password are required.")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return error_response("Invalid credentials.", status_code=401)

    if not user.is_active():
        return error_response("Your account has been deactivated. Contact admin.", status_code=403)


    extra_claims = {
        "user_id": user.id,
        "role":    user.role.value,
        "email":   user.email,
    }

    if user.role == UserRole.COMPANY and user.company_profile:
        extra_claims["is_approved"] = user.company_profile.is_approved()

    token = create_access_token(identity=str(user.id), additional_claims=extra_claims)

    user.last_login = datetime.now(timezone.utc)
    db.session.commit()

    return success_response(
        data={"access_token": token, "role": user.role.value},
        message="Login successful."
    )