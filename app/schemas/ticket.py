from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Campos comunes que el cliente puede enviar y editar
class TicketEditable(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    fecha_ingreso_solicitud: Optional[datetime] = None
    fecha_realizar_servicio: Optional[datetime] = None
    fecha_termino_servicio: Optional[datetime] = None
    # Relaciones (hazlas opcionales si el front no siempre las manda)
    id_status: Optional[int] = None
    id_priority: Optional[int] = None
    id_type: Optional[int] = None
    id_category: Optional[int] = None

class TicketCreate(TicketEditable):
    # Campos de control del backend/negocio
    id_managing_user: Optional[int] = None
    id_customer: Optional[int] = None
    user_id: Optional[int] = None

class TicketUpdate(TicketEditable):
    id_managing_user: Optional[int] = None
    id_customer: Optional[int] = None
    user_id: Optional[int] = None

# Payloads de salida (incluyen audit fields)
class TicketBaseOut(TicketEditable):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Pydantic v2

class Ticket(TicketBaseOut):
    pass
