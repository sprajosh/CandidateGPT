from datetime import datetime, timezone

from sqlalchemy import ARRAY, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.db.models.application import Application  # Ensure this import exists


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    location = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    required_skills = Column(ARRAY(String))

    applications = relationship(Application, back_populates="opportunity")
