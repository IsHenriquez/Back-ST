from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    fecha_ingreso_solicitud: Optional[datetime] = None
    fecha_realizar_servicio: Optional[datetime] = None
    fecha_termino_servicio: Optional[datetime] = None

class TicketCreate(TicketBase):
    pass

class TicketUpdate(TicketBase):
    pass

class TicketInDBBase(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Ticket(TicketInDBBase):
    pass
