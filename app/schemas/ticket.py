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
    id_status: Optional[int] = None
    id_priority: Optional[int] = None
    id_type: Optional[int] = None
    id_category: Optional[int] = None


class TicketCreate(TicketBase):
    id_managing_user: int
    id_status: int
    id_type: int
    id_category: int
    id_priority: int
    id_customer: Optional[int] = None
    user_id: Optional[int] = None


class TicketUpdate(TicketBase):
    id_managing_user: Optional[int] = None
    id_status: Optional[int] = None
    id_type: Optional[int] = None
    id_category: Optional[int] = None
    id_priority: Optional[int] = None
    id_customer: Optional[int] = None
    user_id: Optional[int] = None

class TicketInDBBase(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Ticket(TicketBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # pydantic v2
