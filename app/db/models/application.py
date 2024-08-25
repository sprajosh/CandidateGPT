from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class ApplicationStatus(Enum):
    APPLIED = "applied"
    INTERVIEWED = "interviewed"
    OFFERED = "offered"
    REJECTED = "rejected"
    HIRED = "hired"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"))
    applied_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(SqlEnum(ApplicationStatus), default=ApplicationStatus.APPLIED)

    candidate = relationship("Candidate", back_populates="applications")
    opportunity = relationship("Opportunity", back_populates="applications")
