from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class TicketCategoryCreate(TicketCategoryBase):
    pass

class TicketCategoryUpdate(TicketCategoryBase):
    pass

class TicketCategoryInDBBase(TicketCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TicketCategory(TicketCategoryInDBBase):
    pass
