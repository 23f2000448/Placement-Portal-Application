from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_mail import Mail
from sqlalchemy import event
from sqlalchemy.orm import Mapper
from datetime import datetime, timezone

db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
mail = Mail()



def _set_updated_at(mapper, connection, target):
    if hasattr(target, "updated_at"):
        target.updated_at = datetime.now(timezone.utc)

event.listen(Mapper, "before_update", _set_updated_at)