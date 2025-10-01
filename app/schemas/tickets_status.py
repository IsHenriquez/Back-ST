from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketsStatusBase(BaseModel):
    name: str
    description: Optional[str] = None

class TicketsStatusCreate(TicketsStatusBase):
    pass

class TicketsStatusUpdate(TicketsStatusBase):
    pass

class TicketsStatusInDBBase(TicketsStatusBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TicketsStatus(TicketsStatusInDBBase):
    pass
