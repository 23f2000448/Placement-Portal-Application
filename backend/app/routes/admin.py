from flask import Blueprint, request
from app.utils.decorators import admin_required
from app.utils.responses import success_response, error_response
from app.services import admin_service
from app.schemas.company import CompanySchema
from app.schemas.student import StudentSchema
from app.schemas.placement_drive import PlacementDriveSchema
from app.schemas.application import ApplicationSchema

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

company_schema    = CompanySchema()
companies_schema  = CompanySchema(many=True)
student_schema    = StudentSchema()
students_schema   = StudentSchema(many=True)
drive_schema      = PlacementDriveSchema()
drives_schema     = PlacementDriveSchema(many=True)
applications_schema = ApplicationSchema(many=True)


@admin_bp.route("/dashboard", methods=["GET"])
@admin_required
def dashboard():
    stats = admin_service.get_dashboard_stats()
    return success_response(data=stats, message="Dashboard stats fetched.")


@admin_bp.route("/companies", methods=["GET"])
@admin_required
def list_companies():
    companies = admin_service.get_companies(
        search=request.args.get("search"),
        approval_status=request.args.get("approval_status")
    )
    return success_response(data=companies_schema.dump(companies), message="Companies fetched.")


@admin_bp.route("/companies/<int:company_id>/action", methods=["PATCH"])
@admin_required
def company_action(company_id):
    body   = request.get_json(silent=True) or {}
    action = body.get("action")
    if action not in ("approve", "reject", "blacklist", "deactivate", "activate"):
        return error_response("Invalid action.", status_code=400)
    company = admin_service.update_company_approval(company_id, action)
    return success_response(data=company_schema.dump(company), message=f"Company {action}d.")


@admin_bp.route("/students", methods=["GET"])
@admin_required
def list_students():
    students = admin_service.get_students(search=request.args.get("search"))
    return success_response(data=students_schema.dump(students), message="Students fetched.")


@admin_bp.route("/students/<int:student_id>/action", methods=["PATCH"])
@admin_required
def student_action(student_id):
    body   = request.get_json(silent=True) or {}
    action = body.get("action")
    if action not in ("blacklist", "deactivate", "activate"):
        return error_response("Invalid action.", status_code=400)
    try:
        student = admin_service.update_student_status(student_id, action)
    except ValueError as e:
        return error_response(str(e), status_code=400)
    return success_response(data=student_schema.dump(student), message=f"Student {action}d.")


@admin_bp.route("/drives", methods=["GET"])
@admin_required
def list_drives():
    drives = admin_service.get_drives(status=request.args.get("status"))
    return success_response(data=drives_schema.dump(drives), message="Drives fetched.")


@admin_bp.route("/drives/<int:drive_id>/action", methods=["PATCH"])
@admin_required
def drive_action(drive_id):
    body   = request.get_json(silent=True) or {}
    action = body.get("action")
    if action not in ("approve", "reject", "close"):
        return error_response("Invalid action.", status_code=400)
    try:
        drive = admin_service.update_drive_status(drive_id, action)
    except ValueError as e:
        return error_response(str(e), status_code=400)
    return success_response(data=drive_schema.dump(drive), message=f"Drive {action}d.")


@admin_bp.route("/applications", methods=["GET"])
@admin_required
def list_applications():
    apps = admin_service.get_all_applications()
    return success_response(data=applications_schema.dump(apps), message="Applications fetched.")