from app.extensions import ma
from app.models.user import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = False
        fields = ("id", "email", "role", "status")

    role   = ma.Function(lambda obj: obj.role.value)
    status = ma.Function(lambda obj: obj.status.value)