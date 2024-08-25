from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.database import Base, engine
from app.db.models.application import Application, ApplicationStatus
from app.db.models.candidate import Candidate
from app.db.models.opportunity import Opportunity


def create_sample_data(db: Session):
    opportunity1 = Opportunity(
        title="Software Engineer",
        description="Develop cool stuff",
        location="New York",
        created_at=datetime.now(timezone.utc),
        required_skills=["Python", "FastAPI"],
    )
    opportunity2 = Opportunity(
        title="Data Scientist",
        description="Analyze data and build models",
        location="San Francisco",
        created_at=datetime.now(timezone.utc),
        required_skills=["Python", "Machine Learning"],
    )

    db.add(opportunity1)
    db.add(opportunity2)
    db.commit()

    candidate1 = Candidate(
        name="Alice Johnson",
        email="alice@example.com",
        resume_url="http://example.com/resume_alice.pdf",
        created_at=datetime.now(timezone.utc),
        skills=["Python", "FastAPI", "Machine Learning"],
    )
    candidate2 = Candidate(
        name="Bob Smith",
        email="bob@example.com",
        resume_url="http://example.com/resume_bob.pdf",
        created_at=datetime.now(timezone.utc),
        skills=["Python", "Data Analysis"],
    )

    db.add(candidate1)
    db.add(candidate2)
    db.commit()

    application1 = Application(
        candidate_id=candidate1.id,
        opportunity_id=opportunity1.id,
        status=ApplicationStatus.APPLIED,
        applied_at=datetime.now(timezone.utc),
    )
    application2 = Application(
        candidate_id=candidate2.id,
        opportunity_id=opportunity2.id,
        status=ApplicationStatus.APPLIED,
        applied_at=datetime.now(timezone.utc),
    )

    db.add(application1)
    db.add(application2)
    db.commit()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        create_sample_data(session)
