import os
import click
from flask.cli import with_appcontext
from app.extensions import db
from app.models.user import User, UserRole, UserStatus


def register_commands(app):
    app.cli.add_command(seed_admin_cmd)


@click.command("seed-admin")
@with_appcontext
def seed_admin_cmd():
    existing = User.query.filter_by(role=UserRole.ADMIN).first()

    if existing:
        click.echo(f"Admin already exists ({existing.email}), skipping.")
        return

    admin = User(
        email=os.environ.get("ADMIN_EMAIL", "admin@ppa.com"),
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE,
    )
    admin.set_password(os.environ.get("ADMIN_PASSWORD", "admin123"))
    db.session.add(admin)
    db.session.commit()
    click.echo(f"Admin created: {admin.email}")