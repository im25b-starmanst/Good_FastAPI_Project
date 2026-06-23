from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import models
from database import SessionLocal

router = APIRouter(prefix="/kategorie", tags=["Kategorie"])


class KategorieBase(BaseModel):
    kategorie: str
    istAktiv: bool


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_kategorie(kategorie: KategorieBase, db: db_dependency):
    db_kategorie = models.Kategorie(**kategorie.dict())
    db.add(db_kategorie)
    db.commit()

@router.get("/{kategorieID}", status_code=status.HTTP_200_OK)
async def read_kategorie(kategorieID: int, db: db_dependency):
    kategorie = db.query(models.Kategorie).filter(models.Kategorie.kategorieID == kategorieID).first()
    if kategorie is None:
        raise HTTPException(status_code=404, detail="Kategorie not found")
    return kategorie

@router.delete("/{kategorieID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_kategorie(kategorieID: int, db: db_dependency):
    kategorie = db.query(models.Kategorie).filter(models.Kategorie.kategorieID == kategorieID).first()
    if kategorie is None:
        raise HTTPException(status_code=404, detail="Kategorie not found")
    db.delete(kategorie)
    db.commit()

@router.put("/{kategorieID}", status_code=status.HTTP_200_OK)
async def update_kategorie(kategorieID: int, kategorie: KategorieBase, db: db_dependency):
    db_kategorie = db.query(models.Kategorie).filter(models.Kategorie.kategorieID == kategorieID).first()
    if db_kategorie is None:
        raise HTTPException(status_code=404, detail="Kategorie not found")
    for key, value in kategorie.dict().items():
        setattr(db_kategorie, key, value)
    db.commit()
    return db_kategorie