from app.extensions import db
from datetime import datetime, timezone


class DriveEligibleBranch(db.Model):
    __tablename__ = "drive_eligible_branches"

    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)
    branch = db.Column(db.String(100), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("drive_id", "branch", name="uq_drive_branch"),
        db.Index("ix_drive_eligible_branches_drive_id", "drive_id"),
    )

    drive = db.relationship("PlacementDrive", back_populates="branch_entries")

    def __repr__(self):
        return f"<DriveEligibleBranch drive={self.drive_id} branch={self.branch}>"


class DriveEligibleYear(db.Model):
    __tablename__ = "drive_eligible_years"

    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("drive_id", "year", name="uq_drive_year"),
        db.Index("ix_drive_eligible_years_drive_id", "drive_id"),
    )

    drive = db.relationship("PlacementDrive", back_populates="year_entries")

    def __repr__(self):
        return f"<DriveEligibleYear drive={self.drive_id} year={self.year}>"


class PlacementDrive(db.Model):
    __tablename__ = "placement_drives"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    job_title = db.Column(db.String(200), nullable=False)
    job_description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(150), nullable=True)
    salary_lpa = db.Column(db.Float, nullable=True)

    min_cgpa = db.Column(db.Float, nullable=True)

    application_deadline = db.Column(db.DateTime, nullable=False)

    status = db.Column(
        db.String(20),
        db.CheckConstraint("status IN ('pending','approved','closed','rejected')"),
        default="pending",
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    company = db.relationship("Company", back_populates="placement_drives")
    applications = db.relationship("Application", back_populates="drive", lazy="dynamic")
    branch_entries = db.relationship(
        "DriveEligibleBranch", back_populates="drive",
        cascade="all, delete-orphan", lazy="dynamic"
    )
    year_entries = db.relationship(
        "DriveEligibleYear", back_populates="drive",
        cascade="all, delete-orphan", lazy="dynamic"
    )

    @property
    def eligible_branches_list(self) -> list[str]:
        return [e.branch for e in self.branch_entries]

    @property
    def eligible_years_list(self) -> list[int]:
        return [e.year for e in self.year_entries]

    def set_eligible_branches(self, branches: list[str]) -> None:
        incoming = {b.strip().lower() for b in branches if b.strip()}
        existing = {e.branch.lower(): e for e in self.branch_entries}

        for branch, entry in existing.items():
            if branch not in incoming:
                db.session.delete(entry)

        for branch in incoming:
            if branch not in existing:
                db.session.add(DriveEligibleBranch(drive_id=self.id, branch=branch))

    def set_eligible_years(self, years: list[int]) -> None:
        incoming = set(years)
        existing = {e.year: e for e in self.year_entries}

        for year, entry in existing.items():
            if year not in incoming:
                db.session.delete(entry)

        for year in incoming:
            if year not in existing:
                db.session.add(DriveEligibleYear(drive_id=self.id, year=year))

    def is_open(self) -> bool:
        return (
            self.status == "approved"
            and self.application_deadline > datetime.now(timezone.utc)
        )

    def __repr__(self):
        return f"<PlacementDrive {self.job_title} [{self.status}]>"