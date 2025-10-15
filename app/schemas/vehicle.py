from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VehicleBase(BaseModel):
    plate: str
    description: Optional[str] = None
    id_vehicle_model: Optional[int] = None
    is_busy: Optional[bool] = False
    active: Optional[bool] = True

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    plate: Optional[str] = None
    description: Optional[str] = None
    id_vehicle_model: Optional[int] = None
    is_busy: Optional[bool] = None
    active: Optional[bool] = None

class VehicleOut(VehicleBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
