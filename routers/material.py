from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import models
from database import SessionLocal

router = APIRouter(prefix="/material", tags=["Material"])


class MaterialBase(BaseModel):
    material: str
    istAktiv: bool


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_material(material: MaterialBase, db: db_dependency):
    db_material = models.Material(**material.dict())
    db.add(db_material)
    db.commit()

@router.get("/{materialID}", status_code=status.HTTP_200_OK)
async def read_material(materialID: int, db: db_dependency):
    material = db.query(models.Material).filter(models.Material.materialID == materialID).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@router.delete("/{materialID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_material(materialID: int, db: db_dependency):
    material = db.query(models.Material).filter(models.Material.materialID == materialID).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    db.delete(material)
    db.commit()

@router.put("/{materialID}", status_code=status.HTTP_200_OK)
async def update_material(materialID: int, material: MaterialBase, db: db_dependency):
    db_material = db.query(models.Material).filter(models.Material.materialID == materialID).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    for key, value in material.dict().items():
        setattr(db_material, key, value)
    db.commit()
    return db_material