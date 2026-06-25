from app.extensions import ma
from app.models.interview import Interview


class InterviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Interview
        load_instance = False
        fields = (
            "id", "application_id", "scheduled_at",
            "mode", "venue_or_link", "notes", "result", "created_at"
        )