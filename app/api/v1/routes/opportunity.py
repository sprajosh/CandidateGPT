from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import database, models
from app.schemas import opportunity as schemas

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Opportunity)
def create_opportunity(
    opportunity: schemas.OpportunityCreate, db: Session = Depends(get_db)
):
    db_opportunity = models.Opportunity(**opportunity.model_dump())
    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity


@router.get("/", response_model=list[schemas.Opportunity])
def get_opportunities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Opportunity).offset(skip).limit(limit).all()


@router.get("/{opportunity_id}", response_model=schemas.Opportunity)
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    db_opportunity = (
        db.query(models.Opportunity)
        .filter(models.Opportunity.id == opportunity_id)
        .first()
    )
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return db_opportunity


@router.put("/{opportunity_id}", response_model=schemas.Opportunity)
def update_opportunity(
    opportunity_id: int,
    opportunity: schemas.OpportunityUpdate,
    db: Session = Depends(get_db),
):
    db_opportunity = (
        db.query(models.Opportunity)
        .filter(models.Opportunity.id == opportunity_id)
        .first()
    )
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    for key, value in opportunity.model_dump().items():
        setattr(db_opportunity, key, value)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity


@router.delete("/{opportunity_id}")
def delete_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    db_opportunity = (
        db.query(models.Opportunity)
        .filter(models.Opportunity.id == opportunity_id)
        .first()
    )
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    db.delete(db_opportunity)
    db.commit()
    return {"message": "Opportunity deleted"}
