from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy import text
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from routers import material

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class MaterialBase(BaseModel):
    material: str
    istAktiv: bool

class KategorieBase(BaseModel):
    kategorie: str
    istAktiv: bool
class PrioritaetBase(BaseModel):
    prioritaet: str

class FortschrittBase(BaseModel):
    fortschritt: str

class BenutzerBase(BaseModel):
    benutzername: str
    benutzerPWD: str

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

class DateiBase(BaseModel):
    aufgabeID: int
    dateipfad: str | None = None
    dateiBLOB: bytes | None = None

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

@app.get("/select/all/{table_name}", status_code=status.HTTP_200_OK)
async def select_all(table_name: str, db: db_dependency):
    try:
        result = db.execute(text(f"SELECT * FROM {table_name}"))
        return result.mappings().all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Material Endpoints
@app.post("/material/", status_code=status.HTTP_201_CREATED)
async def create_material(material: MaterialBase, db: db_dependency):
    db_material = models.Material(**material.dict())
    db.add(db_material)
    db.commit()

@app.get("/material/{materialID}", status_code=status.HTTP_200_OK)
async def read_material(materialID: int, db: db_dependency):
    material = db.query(models.Material).filter(models.Material.materialID == materialID).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@app.delete("/material/{materialID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_material(materialID: int, db: db_dependency): 
    material = db.query(models.Material).filter(models.Material.materialID == materialID).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    db.delete(material)
    db.commit()

@app.put("/material/{materialID}", status_code=status.HTTP_200_OK)
async def update_material(materialID: int, material: MaterialBase, db: db_dependency):
    db_material = db.query(models.Material).filter(models.Material.materialID == materialID).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    for key, value in material.dict().items():
        setattr(db_material, key, value)
    db.commit()
    return db_material


# Kategorie Endpoints
@app.post("/kategorie/", status_code=status.HTTP_201_CREATED)
async def create_kategorie(kategorie: KategorieBase, db: db_dependency):
    db_kategorie = models.Kategorie(**kategorie.dict())
    db.add(db_kategorie)
    db.commit()

@app.get("/kategorie/{kategorieID}", status_code=status.HTTP_200_OK)
async def read_kategorie(kategorieID: int, db: db_dependency):
    kategorie = db.query(models.Kategorie).filter(models.Kategorie.kategorieID == kategorieID).first()
    if kategorie is None:
        raise HTTPException(status_code=404, detail="Kategorie not found")
    return kategorie

@app.delete("/kategorie/{kategorieID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_kategorie(kategorieID: int, db: db_dependency):
    kategorie = db.query(models.Kategorie).filter(models.Kategorie.kategorieID == kategorieID).first()
    if kategorie is None:
        raise HTTPException(status_code=404, detail="Kategorie not found")
    db.delete(kategorie)
    db.commit()

@app.put("/kategorie/{kategorieID}", status_code=status.HTTP_200_OK)
async def update_kategorie(kategorieID: int, kategorie: KategorieBase, db: db_dependency):
    db_kategorie = db.query(models.Kategorie).filter(models.Kategorie.kategorieID == kategorieID).first()
    if db_kategorie is None:
        raise HTTPException(status_code=404, detail="Kategorie not found")
    for key, value in kategorie.dict().items():
        setattr(db_kategorie, key, value)
    db.commit()
    return db_kategorie


# Prioritaet Endpoints
@app.post("/prioritaet/", status_code=status.HTTP_201_CREATED)
async def create_prioritaet(prioritaet: PrioritaetBase, db: db_dependency):
    db_prioritaet = models.Prioritaet(**prioritaet.dict())
    db.add(db_prioritaet)
    db.commit()

@app.get("/prioritaet/{prioritaetID}", status_code=status.HTTP_200_OK)
async def read_prioritaet(prioritaetID: int, db: db_dependency):
    prioritaet = db.query(models.Prioritaet).filter(models.Prioritaet.prioritaetID == prioritaetID).first()
    if prioritaet is None:
        raise HTTPException(status_code=404, detail="Priorität not found")
    return prioritaet

@app.delete("/prioritaet/{prioritaetID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prioritaet(prioritaetID: int, db: db_dependency):
    prioritaet = db.query(models.Prioritaet).filter(models.Prioritaet.prioritaetID == prioritaetID).first()
    if prioritaet is None:
        raise HTTPException(status_code=404, detail="Priorität not found")
    db.delete(prioritaet)
    db.commit()

@app.put("/prioritaet/{prioritaetID}", status_code=status.HTTP_200_OK)
async def update_prioritaet(prioritaetID: int, prioritaet: PrioritaetBase, db: db_dependency):
    db_prioritaet = db.query(models.Prioritaet).filter(models.Prioritaet.prioritaetID == prioritaetID).first()
    if db_prioritaet is None:
        raise HTTPException(status_code=404, detail="Priorität not found")
    for key, value in prioritaet.dict().items():
        setattr(db_prioritaet, key, value)
    db.commit()
    return db_prioritaet

# Fortschritt Endpoints
@app.post("/fortschritt/", status_code=status.HTTP_201_CREATED)
async def create_fortschritt(fortschritt: FortschrittBase, db: db_dependency):
    db_fortschritt = models.Fortschritt(**fortschritt.dict())
    db.add(db_fortschritt)
    db.commit()

@app.get("/fortschritt/{fortschrittID}", status_code=status.HTTP_200_OK)
async def read_fortschritt(fortschrittID: int, db: db_dependency):
    fortschritt = db.query(models.Fortschritt).filter(models.Fortschritt.fortschrittID == fortschrittID).first()
    if fortschritt is None:
        raise HTTPException(status_code=404, detail="Fortschritt not found")
    return fortschritt

@app.delete("/fortschritt/{fortschrittID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fortschritt(fortschrittID: int, db: db_dependency):
    fortschritt = db.query(models.Fortschritt).filter(models.Fortschritt.fortschrittID == fortschrittID).first()
    if fortschritt is None:
        raise HTTPException(status_code=404, detail="Fortschritt not found")
    db.delete(fortschritt)
    db.commit()

@app.put("/fortschritt/{fortschrittID}", status_code=status.HTTP_200_OK)
async def update_fortschritt(fortschrittID: int, fortschritt: FortschrittBase, db: db_dependency):
    db_fortschritt = db.query(models.Fortschritt).filter(models.Fortschritt.fortschrittID == fortschrittID).first()
    if db_fortschritt is None:
        raise HTTPException(status_code=404, detail="Fortschritt not found")
    for key, value in fortschritt.dict().items():
        setattr(db_fortschritt, key, value)
    db.commit()
    return db_fortschritt

# Benutzer Endpoints
@app.post("/benutzer/", status_code=status.HTTP_201_CREATED)
async def create_user(benutzer: BenutzerBase, db: db_dependency):
    db_user = models.Benutzer(**benutzer.dict())
    db.add(db_user)
    db.commit()

@app.get("/benutzer/{benutzerID}", status_code=status.HTTP_200_OK)
async def read_benutzer(benutzerID: int, db: db_dependency):
    user =db.query(models.Benutzer).filter(models.Benutzer.benutzerID == benutzerID).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/benutzer/{benutzerID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_benutzer(benutzerID: int, db: db_dependency):
    user = db.query(models.Benutzer).filter(models.Benutzer.benutzerID == benutzerID).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

@app.put("/benutzer/{benutzerID}", status_code=status.HTTP_200_OK)
async def update_benutzer(benutzerID: int, benutzer: BenutzerBase, db: db_dependency):
    db_user = db.query(models.Benutzer).filter(models.Benutzer.benutzerID == benutzerID).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in benutzer.dict().items():
        setattr(db_user, key, value)
    db.commit()
    return db_user


# Aufgabe Endpoints
@app.post("/aufgabe/", status_code=status.HTTP_201_CREATED)
async def create_aufgabe(aufgabe: AufgabeBase, db: db_dependency):
    db_aufgabe = models.Aufgabe(**aufgabe.dict())
    db.add(db_aufgabe)
    db.commit()

@app.get("/aufgabe/{aufgabeID}", status_code=status.HTTP_200_OK)
async def read_aufgabe(aufgabeID: int, db: db_dependency):
    aufgabe = db.query(models.Aufgabe).filter(models.Aufgabe.aufgabeID == aufgabeID).first()
    if aufgabe is None:
        raise HTTPException(status_code=404, detail="Aufgabe not found")
    return aufgabe

@app.delete("/aufgabe/{aufgabeID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aufgabe(aufgabeID: int, db: db_dependency):
    aufgabe = db.query(models.Aufgabe).filter(models.Aufgabe.aufgabeID == aufgabeID).first()
    if aufgabe is None:
        raise HTTPException(status_code=404, detail="Aufgabe not found")
    db.delete(aufgabe)
    db.commit()

@app.put("/aufgabe/{aufgabeID}", status_code=status.HTTP_200_OK)
async def update_aufgabe(aufgabeID: int, aufgabe: AufgabeBase, db: db_dependency):
    db_aufgabe = db.query(models.Aufgabe).filter(models.Aufgabe.aufgabeID == aufgabeID).first()
    if db_aufgabe is None:
        raise HTTPException(status_code=404, detail="Aufgabe not found")
    for key, value in aufgabe.dict().items():
        setattr(db_aufgabe, key, value)
    db.commit()
    return db_aufgabe

# Datei Endpoints
@app.post("/datei/", status_code=status.HTTP_201_CREATED)
async def create_datei(datei: DateiBase, db: db_dependency):
    db_datei = models.Datei(**datei.dict())
    db.add(db_datei)
    db.commit()


@app.get("/datei/{dateiID}", status_code=status.HTTP_200_OK)
async def read_datei(dateiID: int, db: db_dependency):
    datei = db.query(models.Datei).filter(models.Datei.dateiID == dateiID).first()
    if datei is None:
        raise HTTPException(status_code=404, detail="Datei not found")
    return datei

@app.delete("/datei/{dateiID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_datei(dateiID: int, db: db_dependency):
    datei = db.query(models.Datei).filter(models.Datei.dateiID == dateiID).first()
    if datei is None:
        raise HTTPException(status_code=404, detail="Datei not found")
    db.delete(datei)
    db.commit()

@app.put("/datei/{dateiID}", status_code=status.HTTP_200_OK)
async def update_datei(dateiID: int, datei: DateiBase, db: db_dependency):  
    db_datei = db.query(models.Datei).filter(models.Datei.dateiID == dateiID).first()
    if db_datei is None:
        raise HTTPException(status_code=404, detail="Datei not found")
    for key, value in datei.dict().items():
        setattr(db_datei, key, value)
    db.commit()
    return db_datei


# AufgabeMaterial Endpoints
@app.post("/aufgabematerial/", status_code=status.HTTP_201_CREATED)
async def create_aufgabematerial(aufgabematerial: AufgabeMaterialBase, db: db_dependency):
    db_aufgabematerial = models.AufgabeMaterial(**aufgabematerial.dict())
    db.add(db_aufgabematerial)
    db.commit()


@app.get("/aufgabematerial/{aufgabeID}/{materialID}", status_code=status.HTTP_200_OK)
async def read_aufgabematerial(aufgabeID: int, materialID: int, db: db_dependency):
    aufgabematerial = db.query(models.AufgabeMaterial).filter(models.AufgabeMaterial.aufgabeID == aufgabeID, models.AufgabeMaterial.materialID == materialID).first()
    if aufgabematerial is None:
        raise HTTPException(status_code=404, detail="AufgabeMaterial not found")
    return aufgabematerial

@app.delete("/aufgabematerial/{aufgabeID}/{materialID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aufgabematerial(aufgabeID: int, materialID: int, db: db_dependency):
    aufgabematerial = db.query(models.AufgabeMaterial).filter(models.AufgabeMaterial.aufgabeID == aufgabeID, models.AufgabeMaterial.materialID == materialID).first()
    if aufgabematerial is None:
        raise HTTPException(status_code=404, detail="AufgabeMaterial not found")
    db.delete(aufgabematerial)
    db.commit()

@app.put("/aufgabematerial/{aufgabeID}/{materialID}", status_code=status.HTTP_200_OK)
async def update_aufgabematerial(aufgabeID: int, materialID: int, aufgabematerial: AufgabeMaterialBase, db: db_dependency):
    db_aufgabematerial = db.query(models.AufgabeMaterial).filter(models.AufgabeMaterial.aufgabeID == aufgabeID, models.AufgabeMaterial.materialID == materialID).first()
    if db_aufgabematerial is None:
        raise HTTPException(status_code=404, detail="AufgabeMaterial not found")
    for key, value in aufgabematerial.dict().items():
        setattr(db_aufgabematerial, key, value)
    db.commit()
    return db_aufgabematerial

@app.get('/view/')
async def read_view(db: db_dependency):
    db.execute(text("""
    CREATE OR REPLACE VIEW Benutzeraufgaben AS
    SELECT BENUTZER.BENUTZERNAME, AUFGABE.TITEL, AUFGABE.ORT, AUFGABE.NOTIZ  
    FROM BENUTZER JOIN AUFGABE
	ON BENUTZER.BENUTZERID = AUFGABE.BENUTZERID;
    """))
    db.commit() 
    result = db.execute(text("SELECT * FROM Benutzeraufgaben;"))

    return result.mappings().all()

@app.get("/procedure/{userid}")
async def read_procedure(userid: int, db: db_dependency):
    result = db.execute(
        text("CALL GetAufgabenByUser(:userid)"),
        {"userid": userid}
    )
    return result.mappings().all()