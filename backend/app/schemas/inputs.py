from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime, timezone


class CompanyProfileUpdateSchema(Schema):
    industry        = fields.Str(load_default=None)
    website         = fields.Str(load_default=None)
    description     = fields.Str(load_default=None)
    location        = fields.Str(load_default=None)
    hr_contact_name  = fields.Str(load_default=None)
    hr_contact_phone = fields.Str(load_default=None)


class PlacementDriveCreateSchema(Schema):
    job_title            = fields.Str(required=True, validate=validate.Length(min=1))
    job_description      = fields.Str(load_default=None)
    location             = fields.Str(load_default=None)
    salary_lpa           = fields.Float(load_default=None)
    min_cgpa             = fields.Float(load_default=None, validate=validate.Range(min=0, max=10))
    application_deadline = fields.DateTime(required=True)
    eligible_branches    = fields.List(fields.Str(), load_default=[])
    eligible_years       = fields.List(fields.Int(), load_default=[])

    @validates("application_deadline")
    def validate_deadline(self, value):
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        if value < now:
            raise ValidationError("Application deadline must be in the future.")


class ApplicationStatusUpdateSchema(Schema):
    status = fields.Str(
        required=True,
        validate=validate.OneOf(["shortlisted", "interview", "selected", "rejected"])
    )


class InterviewScheduleSchema(Schema):
    scheduled_at  = fields.DateTime(required=True)
    mode          = fields.Str(load_default="online", validate=validate.OneOf(["online", "offline", "hybrid"]))
    venue_or_link = fields.Str(load_default=None)
    notes         = fields.Str(load_default=None)


class InterviewResultSchema(Schema):
    result = fields.Str(
        required=True,
        validate=validate.OneOf(["selected", "rejected"])
    )


class StudentProfileUpdateSchema(Schema):
    full_name       = fields.Str(load_default=None, validate=validate.Length(min=1))
    phone           = fields.Str(load_default=None)
    date_of_birth   = fields.Date(load_default=None)
    roll_number     = fields.Str(load_default=None)
    branch          = fields.Str(load_default=None)
    year_of_study   = fields.Int(load_default=None, validate=validate.Range(min=1, max=6))
    cgpa            = fields.Float(load_default=None, validate=validate.Range(min=0, max=10))
    graduation_year = fields.Int(load_default=None)
    skills          = fields.List(fields.Str(), load_default=None)