from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import models
from database import SessionLocal

router = APIRouter(prefix="/fortschritt", tags=["Fortschritt"])


class FortschrittBase(BaseModel):
    fortschritt: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_fortschritt(fortschritt: FortschrittBase, db: db_dependency):
    db_fortschritt = models.Fortschritt(**fortschritt.dict())
    db.add(db_fortschritt)
    db.commit()

@router.get("/{fortschrittID}", status_code=status.HTTP_200_OK)
async def read_fortschritt(fortschrittID: int, db: db_dependency):
    fortschritt = db.query(models.Fortschritt).filter(models.Fortschritt.fortschrittID == fortschrittID).first()
    if fortschritt is None:
        raise HTTPException(status_code=404, detail="Fortschritt not found")
    return fortschritt

@router.delete("/{fortschrittID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fortschritt(fortschrittID: int, db: db_dependency):
    fortschritt = db.query(models.Fortschritt).filter(models.Fortschritt.fortschrittID == fortschrittID).first()
    if fortschritt is None:
        raise HTTPException(status_code=404, detail="Fortschritt not found")
    db.delete(fortschritt)
    db.commit()

@router.put("/{fortschrittID}", status_code=status.HTTP_200_OK)
async def update_fortschritt(fortschrittID: int, fortschritt: FortschrittBase, db: db_dependency):
    db_fortschritt = db.query(models.Fortschritt).filter(models.Fortschritt.fortschrittID == fortschrittID).first()
    if db_fortschritt is None:
        raise HTTPException(status_code=404, detail="Fortschritt not found")
    for key, value in fortschritt.dict().items():
        setattr(db_fortschritt, key, value)
    db.commit()
    return db_fortschritt