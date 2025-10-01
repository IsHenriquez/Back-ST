from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketTypeBase(BaseModel):
    name: str
    description: Optional[str] = None

class TicketTypeCreate(TicketTypeBase):
    pass

class TicketTypeUpdate(TicketTypeBase):
    pass

class TicketTypeInDBBase(TicketTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TicketType(TicketTypeInDBBase):
    pass
