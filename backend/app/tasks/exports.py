import csv
import io
from flask_mail import Message
from app.tasks.celery_app import celery
from app.extensions import mail
from app.models.application import Application


@celery.task(name="app.tasks.exports.export_applications_csv", bind=True)
def export_applications_csv(self, student_id, user_email, student_name):
    applications = (
        Application.query
        .filter_by(student_id=student_id)
        .order_by(Application.applied_at.desc())
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Application ID", "Company Name", "Drive Title",
        "Application Status", "Applied At", "Updated At"
    ])

    for app in applications:
        writer.writerow([
            app.id,
            app.drive.company.name if app.drive and app.drive.company else "",
            app.drive.job_title if app.drive else "",
            app.status,
            app.applied_at.isoformat() if app.applied_at else "",
            app.updated_at.isoformat() if app.updated_at else "",
        ])

    csv_content = output.getvalue()

    msg = Message(
        subject="Your Application History Export",
        recipients=[user_email],
        body=f"Dear {student_name},\n\nPlease find your application history attached.\n\nPlacement Portal Team",
    )
    msg.attach("applications.csv", "text/csv", csv_content)

    try:
        mail.send(msg)
    except Exception as e:
        self.retry(exc=e, countdown=60, max_retries=3)

    return {"status": "done", "student_id": student_id}