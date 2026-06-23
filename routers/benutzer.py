from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import models
from database import SessionLocal

router = APIRouter(prefix="/benutzer", tags=["Benutzer"])


class BenutzerBase(BaseModel):
    benutzername: str
    benutzerPWD: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(benutzer: BenutzerBase, db: db_dependency):
    db_user = models.Benutzer(**benutzer.dict())
    db.add(db_user)
    db.commit()

@router.get("/{benutzerID}", status_code=status.HTTP_200_OK)
async def read_benutzer(benutzerID: int, db: db_dependency):
    user = db.query(models.Benutzer).filter(models.Benutzer.benutzerID == benutzerID).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{benutzerID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_benutzer(benutzerID: int, db: db_dependency):
    user = db.query(models.Benutzer).filter(models.Benutzer.benutzerID == benutzerID).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

@router.put("/{benutzerID}", status_code=status.HTTP_200_OK)
async def update_benutzer(benutzerID: int, benutzer: BenutzerBase, db: db_dependency):
    db_user = db.query(models.Benutzer).filter(models.Benutzer.benutzerID == benutzerID).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in benutzer.dict().items():
        setattr(db_user, key, value)
    db.commit()
    return db_user