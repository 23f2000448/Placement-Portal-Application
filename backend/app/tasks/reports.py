from datetime import datetime, timezone
from flask_mail import Message
from app.tasks.celery_app import celery
from app.extensions import mail, db
from app.models.user import User, UserRole
from app.models.placement_drive import PlacementDrive
from app.models.application import Application
from app.models.placement import Placement


@celery.task(name="app.tasks.reports.send_monthly_report")
def send_monthly_report():
    now = datetime.now(timezone.utc)
    first_of_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    if now.month == 1:
        first_of_last_month = first_of_this_month.replace(year=now.year - 1, month=12)
        report_label = f"December {now.year - 1}"
    else:
        first_of_last_month = first_of_this_month.replace(month=now.month - 1)
        report_label = first_of_last_month.strftime("%B %Y")

    drives_count = PlacementDrive.query.filter(
        PlacementDrive.created_at >= first_of_last_month,
        PlacementDrive.created_at < first_of_this_month,
    ).count()

    apps_count = Application.query.filter(
        Application.applied_at >= first_of_last_month,
        Application.applied_at < first_of_this_month,
    ).count()

    selected_count = Application.query.filter(
        Application.applied_at >= first_of_last_month,
        Application.applied_at < first_of_this_month,
        Application.status == "selected",
    ).count()

    placements_count = Placement.query.filter(
        Placement.created_at >= first_of_last_month,
        Placement.created_at < first_of_this_month,
    ).count()

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
        <h2 style="color: #333;">Monthly Placement Report — {report_label}</h2>
        <hr>
        <table width="100%" cellpadding="10" style="border-collapse: collapse;">
            <tr style="background: #f5f5f5;">
                <td><strong>Placement Drives Conducted</strong></td>
                <td align="right">{drives_count}</td>
            </tr>
            <tr>
                <td><strong>Total Applications Received</strong></td>
                <td align="right">{apps_count}</td>
            </tr>
            <tr style="background: #f5f5f5;">
                <td><strong>Students Selected</strong></td>
                <td align="right">{selected_count}</td>
            </tr>
            <tr>
                <td><strong>Placement Records Created</strong></td>
                <td align="right">{placements_count}</td>
            </tr>
        </table>
        <hr>
        <p style="color: #888; font-size: 12px;">
            Generated on {now.strftime('%Y-%m-%d %H:%M UTC')} by Placement Portal.
        </p>
    </body>
    </html>
    """

    admin = User.query.filter_by(role=UserRole.ADMIN).first()
    if not admin:
        return

    msg = Message(
        subject=f"Monthly Placement Report — {report_label}",
        recipients=[admin.email],
        html=html,
    )
    try:
        mail.send(msg)
    except Exception:
        pass