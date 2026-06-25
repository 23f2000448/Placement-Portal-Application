from flask import Blueprint, request
from flask_jwt_extended import get_jwt
from app.utils.decorators import student_required
from app.utils.responses import success_response, error_response
from app.services import student_service
from app.schemas.student import StudentSchema
from app.schemas.application import ApplicationSchema
from app.schemas.placement_drive import PlacementDriveSchema
from app.schemas.inputs import StudentProfileUpdateSchema

student_bp = Blueprint("student", __name__, url_prefix="/api/student")

student_schema        = StudentSchema()
applications_schema   = ApplicationSchema(many=True)
drives_schema         = PlacementDriveSchema(many=True)
application_schema    = ApplicationSchema()
profile_update_schema = StudentProfileUpdateSchema()


@student_bp.route("/profile", methods=["GET"])
@student_required
def get_profile():
    user_id = int(get_jwt()["user_id"])
    student = student_service.get_student_by_user_id(user_id)
    return success_response(data=student_schema.dump(student), message="Profile fetched.")


@student_bp.route("/profile", methods=["PUT"])
@student_required
def update_profile():
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")
    data    = profile_update_schema.load(body)
    user_id = int(get_jwt()["user_id"])
    student = student_service.update_student_profile(user_id, data)
    return success_response(data=student_schema.dump(student), message="Profile updated.")


@student_bp.route("/drives", methods=["GET"])
@student_required
def list_drives():
    drives = student_service.get_approved_drives(
        search=request.args.get("search"),
        branch=request.args.get("branch"),
    )
    return success_response(data=drives_schema.dump(drives), message="Drives fetched.")


@student_bp.route("/drives/<int:drive_id>/apply", methods=["POST"])
@student_required
def apply(drive_id):
    user_id = int(get_jwt()["user_id"])
    try:
        application = student_service.apply_for_drive(user_id, drive_id)
    except ValueError as e:
        return error_response(str(e), status_code=400)
    return success_response(
        data=application_schema.dump(application),
        message="Applied successfully.",
        status_code=201,
    )


@student_bp.route("/applications", methods=["GET"])
@student_required
def my_applications():
    user_id = int(get_jwt()["user_id"])
    apps    = student_service.get_student_applications(user_id)
    return success_response(data=applications_schema.dump(apps), message="Applications fetched.")


@student_bp.route("/placements", methods=["GET"])
@student_required
def my_placements():
    user_id = int(get_jwt()["user_id"])
    records = student_service.get_student_placements(user_id)
    result  = [
        {
            "id":           p.id,
            "company_name": p.company.name if p.company else None,
            "position":     p.position,
            "salary_lpa":   p.salary_lpa,
            "joining_date": p.joining_date.isoformat() if p.joining_date else None,
            "status":       p.status,
            "created_at":   p.created_at.isoformat() if p.created_at else None,
        }
        for p in records
    ]
    return success_response(data=result, message="Placement history fetched.")


@student_bp.route("/export", methods=["POST"])
@student_required
def export_applications():
    from app.tasks.exports import export_applications_csv
    from app.models.student import Student

    user_id = int(get_jwt()["user_id"])
    student = Student.query.filter_by(user_id=user_id).first_or_404()
    user    = student.user

    task = export_applications_csv.delay(student.id, user.email, student.full_name)
    return success_response(
        data={"task_id": task.id},
        message="Export started. You will receive an email once done.",
        status_code=202,
    )


@student_bp.route("/export/<task_id>", methods=["GET"])
@student_required
def export_status(task_id):
    from app.tasks.celery_app import celery
    from celery.result import AsyncResult

    result = AsyncResult(task_id, app=celery)
    return success_response(
        data={"task_id": task_id, "status": result.status},
        message="Task status fetched.",
    )