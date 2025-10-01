from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VehicleModelBase(BaseModel):
    id_vehicles_brand: int
    name: str

class VehicleModelCreate(VehicleModelBase):
    pass

class VehicleModelUpdate(VehicleModelBase):
    pass

class VehicleModelInDBBase(VehicleModelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class VehicleModel(VehicleModelInDBBase):
    pass
