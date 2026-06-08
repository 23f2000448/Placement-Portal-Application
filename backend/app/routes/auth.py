import logging
from flask import Blueprint, request, current_app
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from app.extensions import db
from app.models.user import User, UserRole, UserStatus
from app.models.company import Company
from app.models.student import Student
from app.schemas import StudentSchema, CompanySchema
from app.schemas import StudentRegisterSchema, CompanyRegisterSchema, LoginSchema
from app.utils.responses import success_response, error_response
from datetime import datetime, timezone

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

logger = logging.getLogger(__name__)

student_register_schema = StudentRegisterSchema()
company_register_schema = CompanyRegisterSchema()
login_schema            = LoginSchema()
student_schema          = StudentSchema()
company_schema          = CompanySchema()




@auth_bp.route("/register/student", methods=["POST"])
def register_student():
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")

    try:
        data = student_register_schema.load(body)
    except ValidationError as e:
        return error_response("Validation failed.", errors=e.messages, status_code=422)

    try:
        user = User(
            email=data["email"].lower(),
            role=UserRole.STUDENT,
            status=UserStatus.ACTIVE
        )
        user.set_password(data["password"])
        db.session.add(user)
        db.session.flush()

        student = Student(user_id=user.id, full_name=data["full_name"].strip())
        db.session.add(student)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        return error_response("An account with this email already exists.", status_code=409)

    except Exception:
        db.session.rollback()
        current_app.logger.exception("Unexpected error during student registration")
        return error_response("Registration failed. Please try again.", status_code=500)

    return success_response(
        data=student_schema.dump(student),
        message="Student registered successfully.",
        status_code=201
    )


@auth_bp.route("/register/company", methods=["POST"])
def register_company():
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")

    try:
        data = company_register_schema.load(body)
    except ValidationError as e:
        return error_response("Validation failed.", errors=e.messages, status_code=422)

    try:
        user = User(
            email=data["email"].lower(),
            role=UserRole.COMPANY,
            status=UserStatus.ACTIVE
        )
        user.set_password(data["password"])
        db.session.add(user)
        db.session.flush()

        company = Company(user_id=user.id, name=data["name"].strip())
        db.session.add(company)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        return error_response("An account with this email already exists.", status_code=409)

    except Exception:
        db.session.rollback()
        current_app.logger.exception("Unexpected error during company registration")
        return error_response("Registration failed. Please try again.", status_code=500)

    return success_response(
        data=company_schema.dump(company),
        message="Company registered successfully. Await admin approval.",
        status_code=201
    )



@auth_bp.route("/login", methods=["POST"])
def login():
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")

    try:
        data = login_schema.load(body)
    except ValidationError as e:
        return error_response("Validation failed.", errors=e.messages, status_code=422)

    user = User.query.filter_by(email=data["email"].lower()).first()

    if not user or not user.check_password(data["password"]):
        return error_response("Invalid credentials.", status_code=401)

    if not user.is_active():
        return error_response("Your account has been deactivated. Contact admin.", status_code=403)

    extra_claims = {
        "role":  user.role.value,
        "email": user.email,
    }

    if user.role == UserRole.COMPANY and user.company_profile:
        extra_claims["is_approved"] = user.company_profile.is_approved()

    token = create_access_token(identity=str(user.id), additional_claims=extra_claims)

    try:
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()
    except Exception:
        current_app.logger.exception("Failed to update last_login for user %s", user.id)

    return success_response(
        data={"access_token": token, "role": user.role.value},
        message="Login successful."
    )