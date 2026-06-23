from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import models
from database import SessionLocal

router = APIRouter(prefix="/prioritaet", tags=["Prioritaet"])


class PrioritaetBase(BaseModel):
    prioritaet: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_prioritaet(prioritaet: PrioritaetBase, db: db_dependency):
    db_prioritaet = models.Prioritaet(**prioritaet.dict())
    db.add(db_prioritaet)
    db.commit()

@router.get("/{prioritaetID}", status_code=status.HTTP_200_OK)
async def read_prioritaet(prioritaetID: int, db: db_dependency):
    prioritaet = db.query(models.Prioritaet).filter(models.Prioritaet.prioritaetID == prioritaetID).first()
    if prioritaet is None:
        raise HTTPException(status_code=404, detail="Priorität not found")
    return prioritaet

@router.delete("/{prioritaetID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prioritaet(prioritaetID: int, db: db_dependency):
    prioritaet = db.query(models.Prioritaet).filter(models.Prioritaet.prioritaetID == prioritaetID).first()
    if prioritaet is None:
        raise HTTPException(status_code=404, detail="Priorität not found")
    db.delete(prioritaet)
    db.commit()

@router.put("/{prioritaetID}", status_code=status.HTTP_200_OK)
async def update_prioritaet(prioritaetID: int, prioritaet: PrioritaetBase, db: db_dependency):
    db_prioritaet = db.query(models.Prioritaet).filter(models.Prioritaet.prioritaetID == prioritaetID).first()
    if db_prioritaet is None:
        raise HTTPException(status_code=404, detail="Priorität not found")
    for key, value in prioritaet.dict().items():
        setattr(db_prioritaet, key, value)
    db.commit()
    return db_prioritaet