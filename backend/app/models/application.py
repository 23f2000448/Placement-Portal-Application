from app.extensions import db
from datetime import datetime, timezone


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)

    status = db.Column(
        db.String(20),
        db.CheckConstraint("status IN ('applied','shortlisted','interview','selected','rejected')"),
        default="applied",
        nullable=False
    )

    applied_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="uq_student_drive"),
        db.Index("ix_applications_drive_id", "drive_id"),
        db.Index("ix_applications_student_id", "student_id"),
    )

    student = db.relationship("Student", back_populates="applications")
    drive = db.relationship("PlacementDrive", back_populates="applications")
    interview = db.relationship("Interview", back_populates="application", uselist=False)
    placement = db.relationship("Placement", back_populates="application", uselist=False)

    def __repr__(self):
        return f"<Application student={self.student_id} drive={self.drive_id} [{self.status}]>"