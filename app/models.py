from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

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
