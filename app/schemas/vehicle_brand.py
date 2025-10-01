from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VehicleBrandBase(BaseModel):
    name: str

class VehicleBrandCreate(VehicleBrandBase):
    pass

class VehicleBrandUpdate(VehicleBrandBase):
    pass

class VehicleBrandInDBBase(VehicleBrandBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class VehicleBrand(VehicleBrandInDBBase):
    pass
