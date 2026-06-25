from app.schemas.user import UserSchema
from app.schemas.company import CompanySchema
from app.schemas.student import StudentSchema
from app.schemas.auth import StudentRegisterSchema, CompanyRegisterSchema, LoginSchema
from app.schemas.placement_drive import PlacementDriveSchema
from app.schemas.application import ApplicationSchema
from app.schemas.interview import InterviewSchema
from app.schemas.inputs import (
    CompanyProfileUpdateSchema, PlacementDriveCreateSchema,
    ApplicationStatusUpdateSchema, InterviewScheduleSchema, InterviewResultSchema,
    StudentProfileUpdateSchema
)