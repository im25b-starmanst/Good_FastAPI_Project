from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Text, BLOB
from database import Base


class Material(Base):
    __tablename__ = "material"

    materialID = Column(Integer, primary_key=True, autoincrement=True)
    material = Column(String(100), nullable=False)
    istAktiv = Column(Boolean, nullable=False, default=True)

class Kategorie(Base):
    __tablename__ = "kategorie"

    kategorieID = Column(Integer, primary_key=True, autoincrement=True)
    kategorie = Column(String(100), nullable=False)
    istAktiv = Column(Boolean, nullable=False, default=True)

class Prioritaet(Base):
    __tablename__ = "prioritaet"

    prioritaetID = Column(Integer, primary_key=True, autoincrement=True)
    prioritaet = Column(String(100), nullable=False)

class Fortschritt(Base):
    __tablename__ = "fortschritt"

    fortschrittID = Column(Integer, primary_key=True, autoincrement=True)
    fortschritt = Column(String(100), nullable=False)

class Benutzer(Base):
    __tablename__ = "benutzer"

    benutzerID = Column(Integer, primary_key=True, autoincrement=True)
    benutzername = Column(String(100), nullable=False)
    benutzerPWD = Column(String(100), nullable=False)

class Aufgabe(Base):
    __tablename__ = "aufgabe"

    aufgabeID = Column(Integer, primary_key=True, autoincrement=True)
    titel = Column(String(100), nullable=False)
    beginn = Column(Date, nullable=False)
    ende = Column(Date, nullable=True)
    ort = Column(String(250), nullable=True)
    koordinaten = Column(String(100), nullable=True)
    notizen = Column(Text, nullable=True)
    kategorieID = Column(Integer, ForeignKey("kategorie.kategorieID"), nullable=False)
    prioritaetID = Column(Integer, ForeignKey("prioritaet.prioritaetID"), nullable=False)
    fortschrittID = Column(Integer, ForeignKey("fortschritt.fortschrittID"), nullable=False)
    benutzerID = Column(Integer, ForeignKey("benutzer.benutzerID"), nullable=False)


class Datei(Base):
    __tablename__ = "datei"

    dateiID = Column(Integer, primary_key=True, autoincrement=True)
    aufgabeID = Column(Integer, ForeignKey("aufgabe.aufgabeID"), nullable=False)
    dateipfad = Column(String(250))
    dateiBLOB = Column(BLOB)

class AufgabeMaterial(Base):
    __tablename__ = "aufgabematerial"

    aufgabeID = Column(Integer, ForeignKey("aufgabe.aufgabeID"), primary_key=True)
    materialID = Column(Integer, ForeignKey("material.materialID"), primary_key=True)
    anzahl = Column(Integer, nullable=True)