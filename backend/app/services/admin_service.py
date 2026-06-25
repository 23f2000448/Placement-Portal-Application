from app.extensions import db
from app.models.user import User, UserStatus
from app.models.company import Company
from app.models.student import Student
from app.models.placement_drive import PlacementDrive
from app.models.application import Application


def get_dashboard_stats():
    return {
        "total_students":    Student.query.count(),
        "total_companies":   Company.query.count(),
        "total_drives":      PlacementDrive.query.count(),
        "total_applications": Application.query.count(),
        "pending_companies": Company.query.filter_by(approval_status="pending").count(),
        "pending_drives":    PlacementDrive.query.filter_by(status="pending").count(),
    }


def get_companies(search=None, approval_status=None):
    q = Company.query
    if search:
        q = q.filter(
            db.or_(
                Company.name.ilike(f"%{search}%"),
                Company.industry.ilike(f"%{search}%")
            )
        )
    if approval_status:
        q = q.filter_by(approval_status=approval_status)
    return q.order_by(Company.created_at.desc()).all()


def update_company_approval(company_id, action):
    company = db.get_or_404(Company, company_id)
    if action == "approve":
        company.approval_status = "approved"
    elif action == "reject":
        company.approval_status = "rejected"
    else:
        status_map = {"blacklist": "blacklisted", "deactivate": "inactive", "activate": "active"}
        company.status = status_map[action]
    db.session.commit()
    return company


def get_students(search=None):
    q = Student.query.join(Student.user)
    if search:
        q = q.filter(
            db.or_(
                Student.full_name.ilike(f"%{search}%"),
                Student.roll_number.ilike(f"%{search}%"),
                Student.phone.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )
    return q.order_by(Student.created_at.desc()).all()


def update_student_status(student_id, action):
    student = db.get_or_404(Student, student_id)
    status_map = {"blacklist": "blacklisted", "deactivate": "inactive", "activate": "active"}
    if action not in status_map:
        raise ValueError(f"Invalid action: {action}")
    student.status = status_map[action]
    user_status_map = {
        "blacklist":  UserStatus.BLACKLISTED,
        "deactivate": UserStatus.INACTIVE,
        "activate":   UserStatus.ACTIVE,
    }
    student.user.status = user_status_map[action]
    db.session.commit()
    return student


def get_drives(status=None):
    q = PlacementDrive.query
    if status:
        q = q.filter_by(status=status)
    return q.order_by(PlacementDrive.created_at.desc()).all()


def update_drive_status(drive_id, action):
    drive = db.get_or_404(PlacementDrive, drive_id)
    action_map = {"approve": "approved", "reject": "rejected", "close": "closed"}
    if action not in action_map:
        raise ValueError(f"Invalid action: {action}")
    drive.status = action_map[action]
    db.session.commit()
    return drive


def get_all_applications():
    return Application.query.order_by(Application.applied_at.desc()).all()