from app.extensions import ma
from app.models.company import Company
from app.schemas.user import UserSchema


class CompanySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        load_instance = False
        fields = ("id", "user_id", "name", "approval_status", "status", "user")

    user = ma.Nested(UserSchema, dump_only=True)