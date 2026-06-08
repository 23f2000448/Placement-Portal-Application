from app.extensions import ma
from app.models.student import Student
from app.schemas.user import UserSchema


class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = False
        fields = ("id", "user_id", "full_name", "user")

    user = ma.Nested(UserSchema, dump_only=True)