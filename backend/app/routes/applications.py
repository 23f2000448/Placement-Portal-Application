from flask import Blueprint, request
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from app.utils.decorators import student_required, admin_required
from app.utils.responses import success_response, error_response
from app.extensions import db
from app.models.application import Application
from app.schemas.application import ApplicationSchema

applications_bp = Blueprint("applications", __name__, url_prefix="/api/applications")

application_schema  = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)


@applications_bp.route("/<int:application_id>", methods=["GET"])
def get_application(application_id):
    verify_jwt_in_request()
    claims = get_jwt()
    role   = claims.get("role")

    application = db.get_or_404(Application, application_id)

    if role == "student":
        from app.models.student import Student
        student = Student.query.filter_by(user_id=int(claims["user_id"])).first_or_404()
        if application.student_id != student.id:
            return error_response("Access denied.", status_code=403)

    elif role == "company":
        from app.models.company import Company
        company = Company.query.filter_by(user_id=int(claims["user_id"])).first_or_404()
        if application.drive.company_id != company.id:
            return error_response("Access denied.", status_code=403)

    return success_response(data=application_schema.dump(application), message="Application fetched.")