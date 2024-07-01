from sqlalchemy.orm import Session
from . import models, schemas

def get_car(db: Session, car_id: int):
    return db.query(models.Car).filter(models.Car.id == car_id).first()

def get_cars(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Car).offset(skip).limit(limit).all()

def get_cars_by_brand(db: Session, brand: str):
    return db.query(models.Car).filter(models.Car.brand == brand).all()

def get_cars_by_subsidiary_name(db: Session, subsidiary_name: str):
    return db.query(models.Car).join(models.Subsidiary).filter(models.Subsidiary.name == subsidiary_name).all()

def create_car(db: Session, car: schemas.CarCreate):
    db_car = models.Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car
