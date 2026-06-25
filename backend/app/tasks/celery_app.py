from celery import Celery
from celery.schedules import crontab

celery = Celery()


def init_celery(app):
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        timezone="UTC",
        beat_schedule={
            "daily-reminders": {
                "task": "app.tasks.reminders.send_daily_reminders",
                "schedule": crontab(hour=8, minute=0),
            },
            "monthly-report": {
                "task": "app.tasks.reports.send_monthly_report",
                "schedule": crontab(day_of_month=1, hour=0, minute=0),
            },
        },
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery