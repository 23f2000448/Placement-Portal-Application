from app.extensions import ma
from app.models.application import Application
from marshmallow import fields


class ApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Application
        load_instance = False
        fields = (
            "id", "student_id", "drive_id", "status",
            "applied_at", "updated_at",
            "student_name", "student_roll", "drive_title", "company_name"
        )

    student_name = fields.Method("get_student_name", dump_only=True)
    student_roll = fields.Method("get_student_roll", dump_only=True)
    drive_title  = fields.Method("get_drive_title",  dump_only=True)
    company_name = fields.Method("get_company_name", dump_only=True)

    def get_student_name(self, obj):
        return obj.student.full_name if obj.student else None

    def get_student_roll(self, obj):
        return obj.student.roll_number if obj.student else None

    def get_drive_title(self, obj):
        return obj.drive.job_title if obj.drive else None

    def get_company_name(self, obj):
        return obj.drive.company.name if obj.drive and obj.drive.company else None