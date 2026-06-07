from app.extensions import db
from datetime import datetime, timezone


APPROVAL_STATUSES = ("pending", "approved", "rejected")
COMPANY_STATUSES = ("active", "inactive", "blacklisted")


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)


    name = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(150), nullable=True)
    hr_contact_name = db.Column(db.String(100), nullable=True)
    hr_contact_phone = db.Column(db.String(20), nullable=True)


    approval_status = db.Column(
        db.String(20),
        db.CheckConstraint("approval_status IN ('pending','approved','rejected')"),
        default="pending",
        nullable=False
    )
    status = db.Column(
        db.String(20),
        db.CheckConstraint("status IN ('active','inactive','blacklisted')"),
        default="active",
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship("User", back_populates="company_profile")
    placements = db.relationship("Placement", back_populates="company", lazy="dynamic")
    placement_drives = db.relationship("PlacementDrive", back_populates="company", lazy="dynamic")

    def is_approved(self) -> bool:
        return self.approval_status == "approved" and self.status == "active"

    def __repr__(self):
        return f"<Company {self.name} [{self.approval_status}]>"