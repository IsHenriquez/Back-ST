from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketsPriorityBase(BaseModel):
    name: str
    description: Optional[str] = None

class TicketsPriorityCreate(TicketsPriorityBase):
    pass

class TicketsPriorityUpdate(TicketsPriorityBase):
    pass

class TicketsPriorityInDBBase(TicketsPriorityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TicketsPriority(TicketsPriorityInDBBase):
    pass
