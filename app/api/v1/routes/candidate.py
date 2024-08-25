import asyncio

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import database, models
from app.schemas import candidate as schemas
from app.services.resume_extractor import ResumeExtractor
from app.utils.pdf_validator import validate_pdf

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Candidate)
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(get_db)):
    db_candidate = models.Candidate(**candidate.model_dump())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate


@router.get("/", response_model=list[schemas.Candidate])
def get_candidates(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Candidate).offset(skip).limit(limit).all()


@router.get("/{candidate_id}", response_model=schemas.Candidate)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    db_candidate = (
        db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    )
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate


@router.put("/{candidate_id}", response_model=schemas.Candidate)
def update_candidate(
    candidate_id: int, candidate: schemas.CandidateCreate, db: Session = Depends(get_db)
):
    db_candidate = (
        db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    )
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    for key, value in candidate.model_dump().items():
        setattr(db_candidate, key, value)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate


@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    db_candidate = (
        db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    )
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    db.delete(db_candidate)
    db.commit()
    return {"message": "Candidate deleted"}


@router.post("/{candidate_id}/resume")
async def update_skills(
    candidate_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """
    Update the skills of a known candidate based on their resume.
    """
    await validate_pdf(file)
    db_candidate = (
        db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    )
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")

    try:
        extractor = ResumeExtractor(file)
        await extractor.setup()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the file: {str(e)}",
        )

    response = extractor.run(extract_skills=True)
    db_candidate.skills = response["skills"]
    db.commit()
    db.refresh(db_candidate)
    return db_candidate


@router.post("/resume", response_model=schemas.Candidate)
async def create_candidate_from_resume(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    await validate_pdf(file)
    try:
        extractor = ResumeExtractor(file)
        await extractor.setup()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the file: {str(e)}",
        )
    try:
        candidate_data = extractor.run(
            extract_name=True, extract_email=True, extract_skills=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the file: {str(e)}",
        )
    db_candidate = models.Candidate(**candidate_data)
    try:
        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)
    except IntegrityError as e:
        db.rollback()
        if "candidates_email" in str(e.orig):
            raise HTTPException(
                status_code=400,
                detail=f"Candidate with email {candidate_data['email']} already exists.",
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while creating the candidate.",
            )

    return db_candidate
