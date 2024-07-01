import json
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, crud
from .database import SessionLocal, engine
from .celery_app import celery_app
from .tasks import fetch_weather_data, save_weather_data
import os
import glob
import json
from celery import chain  # Asegúrate de importar chain desde Celery

# Crear las tablas de la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/cars", response_model=List[schemas.Car])
def read_cars(skip: int = 0, limit: int = 10, brand: Optional[str] = None, subsidiary_name: Optional[str] = None, db: Session = Depends(get_db)):
    if brand and subsidiary_name:
        cars = db.query(models.Car).join(models.Subsidiary).filter(
            models.Car.brand == brand, models.Subsidiary.name == subsidiary_name
        ).all()
    elif brand:
        cars = crud.get_cars_by_brand(db, brand=brand)
    elif subsidiary_name:
        cars = crud.get_cars_by_subsidiary_name(db, subsidiary_name=subsidiary_name)
    else:
        cars = crud.get_cars(db, skip=skip, limit=limit)
    return cars

@app.post("/cars", response_model=schemas.Car)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    return crud.create_car(db=db, car=car)


@app.post("/fetch-weather")
def fetch_weather():
    # Ejecutar la cadena de tareas
    task_chain = chain(fetch_weather_data.s() | save_weather_data.s())
    task_chain.apply_async()
    return {"status": "Task initiated"}
    


@app.get("/latest-weather")
def latest_weather():
    list_of_files = glob.glob('/app/data/weather_data_*.json')
    if not list_of_files:
        raise HTTPException(status_code=404, detail="No weather data found")
    latest_file = max(list_of_files, key=os.path.getctime)
    with open(latest_file, 'r') as file:
        data = json.load(file)
    return data
