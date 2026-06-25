from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import Subject, UserRole
from app.schemas.common import ORMModel


class UserCreate(BaseModel):
    email: str
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="Password length is limited to 72 bytes because bcrypt truncates longer values.",
    )
    full_name: str = Field(..., min_length=2, max_length=200)
    subject: Subject


class UserRead(ORMModel):
    id: str
    email: str
    full_name: str
    subject: Subject
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserSubjectUpdate(BaseModel):
    subject: Subject


class UserSessionRead(ORMModel):
    id: str
    email: str
    full_name: str
    subject: Subject
    role: UserRole

