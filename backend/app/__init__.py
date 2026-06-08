from flask import Flask
from app.extensions import db, jwt, cache, mail, ma
from app.config import config_map
import os


def create_app(config_name: str = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    config_name = config_name or os.environ.get("FLASK_ENV", "default")
    app.config.from_object(config_map[config_name])

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app, config={"CACHE_TYPE": "RedisCache", "CACHE_REDIS_URL": app.config["REDIS_URL"]})
    mail.init_app(app)
    ma.init_app(app)

    from app.models import (
        User, Company, Student, StudentSkill,
        PlacementDrive, DriveEligibleBranch, DriveEligibleYear,
        Application, Interview, Placement
    )

    with app.app_context():
        db.create_all()

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from seed import register_commands
    register_commands(app)

    return app