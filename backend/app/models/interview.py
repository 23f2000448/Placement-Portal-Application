from app.extensions import db
from datetime import datetime, timezone


class Interview(db.Model):
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False, unique=True)

    scheduled_at = db.Column(db.DateTime, nullable=False)
    mode = db.Column(
        db.String(20),
        db.CheckConstraint("mode IN ('online','offline','hybrid')"),
        default="online",
        nullable=False
    )
    venue_or_link = db.Column(db.String(300), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    result = db.Column(
        db.String(20),
        db.CheckConstraint("result IN ('pending','selected','rejected')"),
        default="pending",
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    application = db.relationship("Application", back_populates="interview")

    def __repr__(self):
        return f"<Interview app={self.application_id} [{self.result}]>"