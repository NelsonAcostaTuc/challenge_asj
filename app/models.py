from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


""" Sobre Modelos

    1. En ningún caso se le asignó un tipo a las variables. 
    Si bien el ORM será capaz de generar las tablas correspondientes, al no indicar los tipos
    de las variables, la experiencia de desarrollo en estos modelos se degradará.

    2. En general, la práctica aceptada es que los nombres de tablas en bases de datos no estén en plural (cars, subsidiaries).
    Es por ello que las clases (Modelos) indicadas en el ejercicio no lo estan.

"""
class Subsidiary(Base):
    __tablename__ = "subsidiaries" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)  # Especificar tamaño para VARCHAR
    created_at = Column(DateTime, default=datetime.utcnow)

    cars = relationship("Car", back_populates="subsidiary")

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    model = Column(String(255), index=True)  # Especificar tamaño para VARCHAR
    brand = Column(String(255), index=True)  # Especificar tamaño para VARCHAR
    subsidiary_id = Column(Integer, ForeignKey('subsidiaries.id'))
    created_at = Column(DateTime, default=datetime.utcnow) 

    subsidiary = relationship("Subsidiary", back_populates="cars")
