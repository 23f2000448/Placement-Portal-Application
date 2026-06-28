from app.extensions import db
from datetime import datetime, timezone


class Placement(db.Model):

    __tablename__ = "placements"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id"),
        nullable=False, unique=True
    )

    position = db.Column(db.String(200), nullable=False)
    salary_lpa = db.Column(db.Float, nullable=True)
    joining_date = db.Column(db.Date, nullable=True)
    offer_letter_path = db.Column(db.String(300), nullable=True)

    status = db.Column(
        db.String(20),
        db.CheckConstraint("status IN ('offered','accepted','declined','joined')"),
        default="offered",
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    __table_args__ = (
        db.Index("ix_placements_student_id", "student_id"),
        db.Index("ix_placements_company_id", "company_id"),
    )

    student = db.relationship("Student", back_populates="placements")
    company = db.relationship("Company", back_populates="placements")
    application = db.relationship("Application", back_populates="placement")

    def __repr__(self):
        return f"<Placement student={self.student_id} company={self.company_id} [{self.status}]>"