from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import models
from database import SessionLocal

router = APIRouter(prefix="/datei", tags=["Datei"])


class DateiBase(BaseModel):
    aufgabeID: int
    dateipfad: str | None = None
    dateiBLOB: bytes | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_datei(datei: DateiBase, db: db_dependency):
    db_datei = models.Datei(**datei.dict())
    db.add(db_datei)
    db.commit()

@router.get("/{dateiID}", status_code=status.HTTP_200_OK)
async def read_datei(dateiID: int, db: db_dependency):
    datei = db.query(models.Datei).filter(models.Datei.dateiID == dateiID).first()
    if datei is None:
        raise HTTPException(status_code=404, detail="Datei not found")
    return datei

@router.delete("/{dateiID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_datei(dateiID: int, db: db_dependency):
    datei = db.query(models.Datei).filter(models.Datei.dateiID == dateiID).first()
    if datei is None:
        raise HTTPException(status_code=404, detail="Datei not found")
    db.delete(datei)
    db.commit()

@router.put("/{dateiID}", status_code=status.HTTP_200_OK)
async def update_datei(dateiID: int, datei: DateiBase, db: db_dependency):
    db_datei = db.query(models.Datei).filter(models.Datei.dateiID == dateiID).first()
    if db_datei is None:
        raise HTTPException(status_code=404, detail="Datei not found")
    for key, value in datei.dict().items():
        setattr(db_datei, key, value)
    db.commit()
    return db_datei