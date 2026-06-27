from flask import Blueprint, request
from app.utils.responses import success_response
from app.extensions import db, cache
from app.models.placement_drive import PlacementDrive
from app.schemas.placement_drive import PlacementDriveSchema
from app.services.student_service import get_approved_drives

drives_bp = Blueprint("drives", __name__, url_prefix="/api/drives")

drive_schema  = PlacementDriveSchema()
drives_schema = PlacementDriveSchema(many=True)


@drives_bp.route("", methods=["GET"])
def list_drives():
    drives = get_approved_drives(search=request.args.get("search"))
    return success_response(data=drives_schema.dump(drives), message="Drives fetched.")


@drives_bp.route("/<int:drive_id>", methods=["GET"])
@cache.cached(timeout=300)
def get_drive(drive_id):
    drive = db.get_or_404(PlacementDrive, drive_id)
    return success_response(data=drive_schema.dump(drive), message="Drive fetched.")