import os
from flask import Flask
from flask_cors import CORS
from app.extensions import db, jwt, cache, mail, ma
from app.config import config_map


def create_app(config_name: str = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    config_name = config_name or os.environ.get("FLASK_ENV", "default")
    config_obj  = config_map.get(config_name)
    if config_obj is None:
        raise ValueError(
            f"Invalid config name '{config_name}'. "
            f"Valid options are: {', '.join(config_map.keys())}"
        )

    if config_name == "production":
        config_obj.validate()

    app.config.from_object(config_obj)

    os.makedirs(app.instance_path, exist_ok=True)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app, config={"CACHE_TYPE": "RedisCache", "CACHE_REDIS_URL": app.config["REDIS_URL"]})
    mail.init_app(app)
    ma.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        from app.models.user import User
        user_id = jwt_payload.get("user_id")
        if not user_id:
            return True
        user = db.session.get(User, int(user_id))
        return user is None or not user.is_active()

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        from flask import jsonify
        return jsonify({
            "success": False,
            "message": "Your account has been deactivated. Contact admin.",
            "errors": {}
        }), 401

    from app.tasks.celery_app import init_celery
    init_celery(app)

    from app.models import (
        User, Company, Student, StudentSkill,
        PlacementDrive, DriveEligibleBranch, DriveEligibleYear,
        Application, Interview, Placement
    )

    with app.app_context():
        db.create_all()

    from app.utils.errors import register_error_handlers
    register_error_handlers(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.routes.company import company_bp
    app.register_blueprint(company_bp)

    from app.routes.student import student_bp
    app.register_blueprint(student_bp)

    from app.routes.drives import drives_bp
    app.register_blueprint(drives_bp)

    from app.routes.applications import applications_bp
    app.register_blueprint(applications_bp)

    from seed import register_commands
    register_commands(app)

    return app