from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import models
from database import SessionLocal

router = APIRouter(prefix="/aufgabe", tags=["Aufgabe"])


class AufgabeBase(BaseModel):
    titel: str
    beginn: str
    ende: str | None = None
    ort: str | None = None
    koordinaten: str | None = None
    notizen: str | None = None
    kategorieID: int
    prioritaetID: int
    fortschrittID: int
    benutzerID: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_aufgabe(aufgabe: AufgabeBase, db: db_dependency):
    db_aufgabe = models.Aufgabe(**aufgabe.dict())
    db.add(db_aufgabe)
    db.commit()

@router.get("/{aufgabeID}", status_code=status.HTTP_200_OK)
async def read_aufgabe(aufgabeID: int, db: db_dependency):
    aufgabe = db.query(models.Aufgabe).filter(models.Aufgabe.aufgabeID == aufgabeID).first()
    if aufgabe is None:
        raise HTTPException(status_code=404, detail="Aufgabe not found")
    return aufgabe

@router.delete("/{aufgabeID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aufgabe(aufgabeID: int, db: db_dependency):
    aufgabe = db.query(models.Aufgabe).filter(models.Aufgabe.aufgabeID == aufgabeID).first()
    if aufgabe is None:
        raise HTTPException(status_code=404, detail="Aufgabe not found")
    db.delete(aufgabe)
    db.commit()

@router.put("/{aufgabeID}", status_code=status.HTTP_200_OK)
async def update_aufgabe(aufgabeID: int, aufgabe: AufgabeBase, db: db_dependency):
    db_aufgabe = db.query(models.Aufgabe).filter(models.Aufgabe.aufgabeID == aufgabeID).first()
    if db_aufgabe is None:
        raise HTTPException(status_code=404, detail="Aufgabe not found")
    for key, value in aufgabe.dict().items():
        setattr(db_aufgabe, key, value)
    db.commit()
    return db_aufgabe