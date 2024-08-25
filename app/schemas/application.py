from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.db.models.application import ApplicationStatus


class ApplicationBase(BaseModel):
    id: int
    candidate_id: int
    opportunity_id: int
    applied_at: datetime
    status: ApplicationStatus

    class Config:
        from_attributes = True


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    applied_at: Optional[datetime] = None

    class Config:
        from_attributes = True
