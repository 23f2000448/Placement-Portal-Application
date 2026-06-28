from sqlalchemy.orm import joinedload
from app.extensions import db, cache
from app.models.company import Company
from app.models.placement_drive import PlacementDrive
from app.models.application import Application
from app.models.interview import Interview
from app.models.placement import Placement


def get_company_by_user_id(user_id):
    return Company.query.filter_by(user_id=user_id).first_or_404()


def update_company_profile(user_id, data):
    company = Company.query.filter_by(user_id=user_id).first_or_404()
    updatable = ["industry", "website", "description", "location", "hr_contact_name", "hr_contact_phone"]
    for field in updatable:
        if data.get(field) is not None:
            setattr(company, field, data[field])
    db.session.commit()
    return company


@cache.memoize(timeout=300)
def get_company_drives(company_id):
    return (
        PlacementDrive.query
        .filter_by(company_id=company_id)
        .order_by(PlacementDrive.created_at.desc())
        .all()
    )


def create_drive(company_id, data):
    drive = PlacementDrive(
        company_id=company_id,
        job_title=data["job_title"],
        job_description=data.get("job_description"),
        location=data.get("location"),
        salary_lpa=data.get("salary_lpa"),
        min_cgpa=data.get("min_cgpa"),
        application_deadline=data["application_deadline"],
        status="pending",
    )
    db.session.add(drive)
    db.session.flush()

    if data.get("eligible_branches"):
        drive.set_eligible_branches(data["eligible_branches"])
    if data.get("eligible_years"):
        drive.set_eligible_years(data["eligible_years"])

    db.session.commit()
    cache.delete_memoized(get_company_drives, company_id)
    return drive


def _get_own_drive(drive_id, company_id):
    return PlacementDrive.query.filter_by(id=drive_id, company_id=company_id).first_or_404()


def close_drive(drive_id, company_id):
    from app.services.student_service import get_approved_drives
    drive = _get_own_drive(drive_id, company_id)
    drive.status = "closed"
    db.session.commit()
    cache.delete_memoized(get_company_drives, company_id)
    cache.delete_memoized(get_approved_drives)
    return drive


def get_drive_applications(drive_id, company_id):
    _get_own_drive(drive_id, company_id)
    return (
        Application.query
        .filter_by(drive_id=drive_id)
        .options(joinedload(Application.student))
        .order_by(Application.applied_at.desc())
        .all()
    )


def update_application_status(application_id, company_id, status):
    app = (
        Application.query
        .join(Application.drive)
        .filter(Application.id == application_id, PlacementDrive.company_id == company_id)
        .first_or_404()
    )
    app.status = status
    db.session.commit()
    return app


def schedule_interview(application_id, company_id, data):
    app = (
        Application.query
        .join(Application.drive)
        .filter(Application.id == application_id, PlacementDrive.company_id == company_id)
        .first_or_404()
    )
    if app.status != "shortlisted":
        raise ValueError("Application must be shortlisted before scheduling an interview.")
    if app.interview:
        raise ValueError("Interview already scheduled for this application.")

    interview = Interview(
        application_id=application_id,
        scheduled_at=data["scheduled_at"],
        mode=data.get("mode", "online"),
        venue_or_link=data.get("venue_or_link"),
        notes=data.get("notes"),
    )
    app.status = "interview"
    db.session.add(interview)
    db.session.commit()
    return interview


def update_interview_result(interview_id, company_id, result):
    interview = (
        Interview.query
        .join(Interview.application)
        .join(Application.drive)
        .filter(Interview.id == interview_id, PlacementDrive.company_id == company_id)
        .first_or_404()
    )
    interview.result = result
    app = interview.application

    if result == "selected":
        app.status = "selected"
        placement = Placement(
            student_id=app.student_id,
            company_id=company_id,
            application_id=app.id,
            position=app.drive.job_title,
            salary_lpa=app.drive.salary_lpa,
        )
        db.session.add(placement)
    else:
        app.status = "rejected"

    db.session.commit()
    return interview