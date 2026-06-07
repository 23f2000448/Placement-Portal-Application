from app.extensions import db
from datetime import datetime, timezone


class StudentSkill(db.Model):
    __tablename__ = "student_skills"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    skill = db.Column(db.String(100), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("student_id", "skill", name="uq_student_skill"),
    )

    student = db.relationship("Student", back_populates="skill_entries")

    def __repr__(self):
        return f"<StudentSkill student={self.student_id} skill={self.skill}>"


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)

    roll_number = db.Column(db.String(50), unique=True, nullable=True)
    branch = db.Column(db.String(100), nullable=True)
    year_of_study = db.Column(db.Integer, nullable=True)
    cgpa = db.Column(db.Float, nullable=True)
    graduation_year = db.Column(db.Integer, nullable=True)

    resume_path = db.Column(db.String(300), nullable=True)

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

    user = db.relationship("User", back_populates="student_profile")
    applications = db.relationship("Application", back_populates="student", lazy="dynamic")
    placements = db.relationship("Placement", back_populates="student", lazy="dynamic")
    skill_entries = db.relationship(
        "StudentSkill", back_populates="student",
        cascade="all, delete-orphan", lazy="dynamic"
    )


    @property
    def skills_list(self) -> list[str]:
        return [s.skill for s in self.skill_entries]


    def set_skills(self, skills: list[str]) -> None:
        incoming = {s.strip().lower() for s in skills if s.strip()}
        existing = {s.skill.lower(): s for s in self.skill_entries}

        for skill_name, entry in existing.items():
            if skill_name not in incoming:
                db.session.delete(entry)

        for skill_name in incoming:
            if skill_name not in existing:
                db.session.add(StudentSkill(student_id=self.id, skill=skill_name))


    def is_eligible_for(self, drive) -> bool:
        if self.cgpa is not None and drive.min_cgpa is not None:
            if self.cgpa < drive.min_cgpa:
                return False

        allowed_branches = drive.eligible_branches_list
        if allowed_branches:
            if not self.branch or self.branch.lower() not in [b.lower() for b in allowed_branches]:
                return False

        allowed_years = drive.eligible_years_list
        if allowed_years:
            if self.year_of_study not in allowed_years:
                return False

        return True


    def __repr__(self):
        return f"<Student {self.full_name} [{self.roll_number}]>"