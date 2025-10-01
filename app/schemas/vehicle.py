from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VehicleBase(BaseModel):
    id_vehicle_model: int
    is_busy: Optional[bool] = False
    active: Optional[int] = 1
    plate: Optional[str] = None
    description: Optional[str] = None

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(VehicleBase):
    pass

class VehicleInDBBase(VehicleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Vehicle(VehicleInDBBase):
    pass
