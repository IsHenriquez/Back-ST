# app/schemas/schedule.py
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class VisitOut(BaseModel):
    id: int
    client: Optional[str] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    window_from: Optional[datetime] = None
    window_to: Optional[datetime] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
