from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import models
from database import SessionLocal

router = APIRouter(prefix="/aufgabematerial", tags=["AufgabeMaterial"])


class AufgabeMaterialBase(BaseModel):
    aufgabeID: int
    materialID: int
    anzahl: int | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_aufgabematerial(aufgabematerial: AufgabeMaterialBase, db: db_dependency):
    db_aufgabematerial = models.AufgabeMaterial(**aufgabematerial.dict())
    db.add(db_aufgabematerial)
    db.commit()

@router.get("/{aufgabeID}/{materialID}", status_code=status.HTTP_200_OK)
async def read_aufgabematerial(aufgabeID: int, materialID: int, db: db_dependency):
    aufgabematerial = db.query(models.AufgabeMaterial).filter(
        models.AufgabeMaterial.aufgabeID == aufgabeID,
        models.AufgabeMaterial.materialID == materialID
    ).first()
    if aufgabematerial is None:
        raise HTTPException(status_code=404, detail="AufgabeMaterial not found")
    return aufgabematerial

@router.delete("/{aufgabeID}/{materialID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aufgabematerial(aufgabeID: int, materialID: int, db: db_dependency):
    aufgabematerial = db.query(models.AufgabeMaterial).filter(
        models.AufgabeMaterial.aufgabeID == aufgabeID,
        models.AufgabeMaterial.materialID == materialID
    ).first()
    if aufgabematerial is None:
        raise HTTPException(status_code=404, detail="AufgabeMaterial not found")
    db.delete(aufgabematerial)
    db.commit()

@router.put("/{aufgabeID}/{materialID}", status_code=status.HTTP_200_OK)
async def update_aufgabematerial(aufgabeID: int, materialID: int, aufgabematerial: AufgabeMaterialBase, db: db_dependency):
    db_aufgabematerial = db.query(models.AufgabeMaterial).filter(
        models.AufgabeMaterial.aufgabeID == aufgabeID,
        models.AufgabeMaterial.materialID == materialID
    ).first()
    if db_aufgabematerial is None:
        raise HTTPException(status_code=404, detail="AufgabeMaterial not found")
    for key, value in aufgabematerial.dict().items():
        setattr(db_aufgabematerial, key, value)
    db.commit()
    return db_aufgabematerial