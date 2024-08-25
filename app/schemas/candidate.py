from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.application import ApplicationBase


class CandidateBase(BaseModel):
    name: str
    email: str
    resume_url: Optional[str] = None
    skills: Optional[List[str]] = []


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    resume_url: Optional[str] = None
    skills: Optional[List[str]] = None

    class Config:
        from_attributes = True


class Candidate(CandidateBase):
    id: int
    created_at: datetime
    applications: Optional[List[ApplicationBase]] = []

    class Config:
        from_attributes = True
