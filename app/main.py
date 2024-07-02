import json
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, crud
from .database import SessionLocal, engine
from .celery_app import celery_app
from .tasks import fetch_weather_data
import os
import glob
import json
from celery import chain  # Asegúrate de importar chain desde Celery
import asyncio
import httpx

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


app.state.fetch_weather_task = None

@app.post("/fetch-weather")
async def fetch_weather():
    if not app.state.fetch_weather_task:
        app.state.fetch_weather_task = asyncio.create_task(periodic_fetch_weather())
    return {"status": "Task initiated"}

# Función asincrónica para ejecutar el endpoint periódicamente
async def periodic_fetch_weather():
    while True:
        await asyncio.sleep(5)  # Esperar 5 segundos
        task_chain = chain(fetch_weather_data.s())
        task_chain.apply_async()

# Asegúrate de cerrar la tarea periódica al cerrar la aplicación
@app.on_event("shutdown")
async def shutdown_event():
    if app.state.fetch_weather_task:
        app.state.fetch_weather_task.cancel()
        try:
            await app.state.fetch_weather_task
        except asyncio.CancelledError:
            pass


