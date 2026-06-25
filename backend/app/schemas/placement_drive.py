from app.extensions import ma
from app.models.placement_drive import PlacementDrive
from marshmallow import fields


class PlacementDriveSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlacementDrive
        load_instance = False
        fields = (
            "id", "company_id", "job_title", "job_description",
            "location", "salary_lpa", "min_cgpa",
            "application_deadline", "status", "created_at",
            "eligible_branches_list", "eligible_years_list", "company_name"
        )

    eligible_branches_list = fields.List(fields.Str(), dump_only=True)
    eligible_years_list = fields.List(fields.Int(), dump_only=True)
    company_name = fields.Method("get_company_name", dump_only=True)

    def get_company_name(self, obj):
        return obj.company.name if obj.company else None