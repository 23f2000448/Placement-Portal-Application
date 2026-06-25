from app.extensions import ma
from app.models.student import Student
from app.schemas.user import UserSchema
from marshmallow import fields


class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = False
        fields = (
            "id", "user_id", "full_name", "phone", "roll_number",
            "branch", "year_of_study", "cgpa", "graduation_year",
            "status", "created_at", "user", "skills_list"
        )

    user        = ma.Nested(UserSchema, dump_only=True)
    skills_list = fields.List(fields.Str(), dump_only=True)