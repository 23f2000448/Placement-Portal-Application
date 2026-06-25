from app.extensions import db
from app.models.student import Student
from app.models.placement_drive import PlacementDrive
from app.models.application import Application
from app.models.placement import Placement


def get_student_by_user_id(user_id):
    return Student.query.filter_by(user_id=user_id).first_or_404()


def update_student_profile(user_id, data):
    student = Student.query.filter_by(user_id=user_id).first_or_404()
    updatable = ["full_name", "phone", "date_of_birth", "roll_number",
                 "branch", "year_of_study", "cgpa", "graduation_year"]
    for field in updatable:
        if data.get(field) is not None:
            setattr(student, field, data[field])
    if data.get("skills") is not None:
        student.set_skills(data["skills"])
    db.session.commit()
    return student


def get_approved_drives(search=None, branch=None):
    q = PlacementDrive.query.filter_by(status="approved")
    if search:
        q = q.filter(PlacementDrive.job_title.ilike(f"%{search}%"))
    if branch:
        from app.models.placement_drive import DriveEligibleBranch
        q = q.join(PlacementDrive.branch_entries).filter(
            DriveEligibleBranch.branch.ilike(f"%{branch}%")
        )
    return q.order_by(PlacementDrive.created_at.desc()).all()


def apply_for_drive(user_id, drive_id):
    student = Student.query.filter_by(user_id=user_id).first_or_404()
    drive   = db.get_or_404(PlacementDrive, drive_id)

    if drive.status != "approved":
        raise ValueError("This drive is not open for applications.")

    if not drive.is_open():
        raise ValueError("Application deadline has passed.")

    if not student.is_eligible_for(drive):
        raise ValueError("You do not meet the eligibility criteria for this drive.")

    existing = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
    if existing:
        raise ValueError("You have already applied for this drive.")

    application = Application(student_id=student.id, drive_id=drive_id, status="applied")
    db.session.add(application)
    db.session.commit()
    return application


def get_student_applications(user_id):
    student = Student.query.filter_by(user_id=user_id).first_or_404()
    return (
        Application.query
        .filter_by(student_id=student.id)
        .order_by(Application.applied_at.desc())
        .all()
    )


def get_student_placements(user_id):
    student = Student.query.filter_by(user_id=user_id).first_or_404()
    return (
        Placement.query
        .filter_by(student_id=student.id)
        .order_by(Placement.created_at.desc())
        .all()
    )