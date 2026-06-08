from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from sqlalchemy import event
from sqlalchemy.orm import Mapper
from datetime import datetime, timezone

db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
mail = Mail()
ma = Marshmallow()

def _set_updated_at(mapper, connection, target):
    if hasattr(target, "updated_at"):
        target.updated_at = datetime.now(timezone.utc)

event.listen(Mapper, "before_update", _set_updated_at)