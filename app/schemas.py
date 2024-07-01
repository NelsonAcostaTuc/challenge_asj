from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class SubsidiaryBase(BaseModel):
    name: str

class SubsidiaryCreate(SubsidiaryBase):
    pass

class Subsidiary(SubsidiaryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode: True

class CarBase(BaseModel):
    year: int
    model: str
    brand: str
    subsidiary_id: int

class CarCreate(CarBase):
    pass

class Car(CarBase):
    id: int
    created_at: datetime
    subsidiary: Subsidiary

    class Config:
        orm_mode: True
