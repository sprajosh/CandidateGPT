from datetime import datetime, timezone

from sqlalchemy import ARRAY, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    resume_url = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    applications = relationship("Application", back_populates="candidate")
    skills = Column(ARRAY(String))
