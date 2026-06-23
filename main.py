from fastapi import FastAPI, status
from sqlalchemy import text
import models
from database import engine
from dependencies import db_dependency
from routers import (
    material,
    kategorie,
    prioritaet,
    fortschritt,
    benutzer,
    aufgabe,
    datei,
    aufgabematerial,
)

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(material.router)
app.include_router(kategorie.router)
app.include_router(prioritaet.router)
app.include_router(fortschritt.router)
app.include_router(benutzer.router)
app.include_router(aufgabe.router)
app.include_router(datei.router)
app.include_router(aufgabematerial.router)


@app.get("/select/all/{table_name}", status_code=status.HTTP_200_OK)
async def select_all(table_name: str, db: db_dependency):
    from fastapi import HTTPException
    try:
        result = db.execute(text(f"SELECT * FROM {table_name}"))
        return result.mappings().all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/view/")
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