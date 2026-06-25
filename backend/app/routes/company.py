from flask import Blueprint, request
from flask_jwt_extended import get_jwt
from app.utils.decorators import company_required, approved_company_required
from app.utils.responses import success_response, error_response
from app.services import company_service
from app.schemas.company import CompanySchema
from app.schemas.placement_drive import PlacementDriveSchema
from app.schemas.application import ApplicationSchema
from app.schemas.interview import InterviewSchema
from app.schemas.inputs import (
    CompanyProfileUpdateSchema, PlacementDriveCreateSchema,
    ApplicationStatusUpdateSchema, InterviewScheduleSchema, InterviewResultSchema
)

company_bp = Blueprint("company", __name__, url_prefix="/api/company")

company_schema           = CompanySchema()
drive_schema             = PlacementDriveSchema()
drives_schema            = PlacementDriveSchema(many=True)
application_schema       = ApplicationSchema()
applications_schema      = ApplicationSchema(many=True)
interview_schema         = InterviewSchema()

profile_update_schema     = CompanyProfileUpdateSchema()
drive_create_schema       = PlacementDriveCreateSchema()
app_status_schema         = ApplicationStatusUpdateSchema()
interview_schedule_schema = InterviewScheduleSchema()
interview_result_schema   = InterviewResultSchema()


@company_bp.route("/profile", methods=["GET"])
@company_required
def get_profile():
    user_id = int(get_jwt()["user_id"])
    company = company_service.get_company_by_user_id(user_id)
    return success_response(data=company_schema.dump(company), message="Profile fetched.")


@company_bp.route("/profile", methods=["PUT"])
@company_required
def update_profile():
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")
    data    = profile_update_schema.load(body)
    user_id = int(get_jwt()["user_id"])
    company = company_service.update_company_profile(user_id, data)
    return success_response(data=company_schema.dump(company), message="Profile updated.")


@company_bp.route("/drives", methods=["GET"])
@approved_company_required
def list_drives():
    user_id = int(get_jwt()["user_id"])
    company = company_service.get_company_by_user_id(user_id)
    drives  = company_service.get_company_drives(company.id)
    return success_response(data=drives_schema.dump(drives), message="Drives fetched.")


@company_bp.route("/drives", methods=["POST"])
@approved_company_required
def create_drive():
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")
    data    = drive_create_schema.load(body)
    user_id = int(get_jwt()["user_id"])
    company = company_service.get_company_by_user_id(user_id)
    drive   = company_service.create_drive(company.id, data)
    return success_response(
        data=drive_schema.dump(drive),
        message="Drive created. Awaiting admin approval.",
        status_code=201
    )


@company_bp.route("/drives/<int:drive_id>", methods=["PATCH"])
@approved_company_required
def close_drive(drive_id):
    user_id = int(get_jwt()["user_id"])
    company = company_service.get_company_by_user_id(user_id)
    drive   = company_service.close_drive(drive_id, company.id)
    return success_response(data=drive_schema.dump(drive), message="Drive closed.")


@company_bp.route("/drives/<int:drive_id>/applications", methods=["GET"])
@approved_company_required
def drive_applications(drive_id):
    user_id = int(get_jwt()["user_id"])
    company = company_service.get_company_by_user_id(user_id)
    apps    = company_service.get_drive_applications(drive_id, company.id)
    return success_response(data=applications_schema.dump(apps), message="Applications fetched.")


@company_bp.route("/applications/<int:application_id>/status", methods=["PATCH"])
@approved_company_required
def update_application_status(application_id):
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")
    data    = app_status_schema.load(body)
    user_id = int(get_jwt()["user_id"])
    company = company_service.get_company_by_user_id(user_id)
    app     = company_service.update_application_status(application_id, company.id, data["status"])
    return success_response(data=application_schema.dump(app), message="Status updated.")


@company_bp.route("/applications/<int:application_id>/interview", methods=["POST"])
@approved_company_required
def schedule_interview(application_id):
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")
    data    = interview_schedule_schema.load(body)
    user_id = int(get_jwt()["user_id"])
    company = company_service.get_company_by_user_id(user_id)
    try:
        interview = company_service.schedule_interview(application_id, company.id, data)
    except ValueError as e:
        return error_response(str(e), status_code=400)
    return success_response(
        data=interview_schema.dump(interview),
        message="Interview scheduled.",
        status_code=201
    )


@company_bp.route("/interviews/<int:interview_id>/result", methods=["PATCH"])
@approved_company_required
def update_interview_result(interview_id):
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")
    data      = interview_result_schema.load(body)
    user_id   = int(get_jwt()["user_id"])
    company   = company_service.get_company_by_user_id(user_id)
    interview = company_service.update_interview_result(interview_id, company.id, data["result"])
    return success_response(data=interview_schema.dump(interview), message="Result updated.")