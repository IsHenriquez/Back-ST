from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PositionBase(BaseModel):
    id_user: int
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class PositionCreate(PositionBase):
    pass

class PositionUpdate(PositionBase):
    pass

class PositionInDBBase(PositionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Position(PositionInDBBase):
    pass
