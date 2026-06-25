from flask import Blueprint, request
from app.utils.responses import success_response
from app.extensions import db, cache
from app.models.placement_drive import PlacementDrive
from app.schemas.placement_drive import PlacementDriveSchema

drives_bp = Blueprint("drives", __name__, url_prefix="/api/drives")

drive_schema  = PlacementDriveSchema()
drives_schema = PlacementDriveSchema(many=True)


@drives_bp.route("", methods=["GET"])
@cache.cached(timeout=300, query_string=True)
def list_drives():
    search = request.args.get("search")
    q = PlacementDrive.query.filter_by(status="approved")
    if search:
        q = q.filter(PlacementDrive.job_title.ilike(f"%{search}%"))
    drives = q.order_by(PlacementDrive.created_at.desc()).all()
    return success_response(data=drives_schema.dump(drives), message="Drives fetched.")


@drives_bp.route("/<int:drive_id>", methods=["GET"])
@cache.cached(timeout=300)
def get_drive(drive_id):
    drive = db.get_or_404(PlacementDrive, drive_id)
    return success_response(data=drive_schema.dump(drive), message="Drive fetched.")