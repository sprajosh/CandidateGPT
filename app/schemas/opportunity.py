from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from app.schemas.application import ApplicationBase


class OpportunityBase(BaseModel):
    title: str
    description: str
    location: str
    required_skills: List[str]

    class Config:
        from_attributes = True


class OpportunityCreate(OpportunityBase):
    created_at: Optional[datetime] = None


class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    required_skills: Optional[List[str]] = None

    class Config:
        from_attributes = True


class Opportunity(OpportunityBase):
    id: int
    created_at: datetime
    applications: Optional[List[ApplicationBase]] = []

    class Config:
        from_attributes = True
