from datetime import datetime, timezone, timedelta
from flask_mail import Message
from app.tasks.celery_app import celery
from app.extensions import mail, db
from app.models.placement_drive import PlacementDrive
from app.models.interview import Interview


@celery.task(name="app.tasks.reminders.send_daily_reminders")
def send_daily_reminders():
    _remind_application_deadlines()
    _remind_upcoming_interviews()


def _remind_application_deadlines():
    now      = datetime.now(timezone.utc)
    deadline = now + timedelta(hours=48)

    drives = (
        PlacementDrive.query
        .filter(
            PlacementDrive.status == "approved",
            PlacementDrive.application_deadline >= now,
            PlacementDrive.application_deadline <= deadline,
        )
        .all()
    )

    for drive in drives:
        applications = drive.applications.all()
        applied_student_ids = {a.student_id for a in applications}

        for app in applications:
            student = app.student
            if not student:
                continue
            user = student.user
            if not user:
                continue

            msg = Message(
                subject=f"Deadline Reminder: {drive.job_title} at {drive.company.name}",
                recipients=[user.email],
                body=(
                    f"Dear {student.full_name},\n\n"
                    f"The application deadline for {drive.job_title} at {drive.company.name} "
                    f"is approaching: {drive.application_deadline.strftime('%Y-%m-%d %H:%M UTC')}.\n\n"
                    f"Log in to the placement portal to check your application status.\n\n"
                    f"Placement Portal Team"
                ),
            )
            try:
                mail.send(msg)
            except Exception:
                pass


def _remind_upcoming_interviews():
    now      = datetime.now(timezone.utc)
    tomorrow = now + timedelta(hours=24)

    interviews = (
        Interview.query
        .filter(
            Interview.scheduled_at >= now,
            Interview.scheduled_at <= tomorrow,
            Interview.result == "pending",
        )
        .all()
    )

    for interview in interviews:
        app     = interview.application
        student = app.student
        drive   = app.drive

        if not student or not student.user:
            continue

        msg = Message(
            subject=f"Interview Tomorrow: {drive.company.name} — {drive.job_title}",
            recipients=[student.user.email],
            body=(
                f"Dear {student.full_name},\n\n"
                f"You have an interview scheduled tomorrow.\n\n"
                f"Company  : {drive.company.name}\n"
                f"Position : {drive.job_title}\n"
                f"Date/Time: {interview.scheduled_at.strftime('%Y-%m-%d %H:%M UTC')}\n"
                f"Mode     : {interview.mode}\n"
                + (f"Link/Venue: {interview.venue_or_link}\n" if interview.venue_or_link else "")
                + f"\nBest of luck!\n\nPlacement Portal Team"
            ),
        )
        try:
            mail.send(msg)
        except Exception:
            pass