# app/routers/schedule.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.core.database import get_db
from app.models.ticket import Ticket
from app.models.customer import Customer 
from app.schemas.schedule import VisitOut

router = APIRouter()

@router.get("/schedule/today", response_model=List[VisitOut])
def get_today_schedule(user_id: int, db: Session = Depends(get_db)):
    """
    Devuelve las visitas (tickets) asignadas al técnico para el día de hoy
    """
    tz = ZoneInfo("America/Santiago")
    now = datetime.now(tz)
    start = datetime(now.year, now.month, now.day, tzinfo=tz)
    end = start + timedelta(days=1)

    q = (
        db.query(Ticket, Customer)
        .outerjoin(Customer, Ticket.id_customer == Customer.id)
        .filter(Ticket.id_managing_user == user_id)
        .filter(Ticket.fecha_realizar_servicio >= start)
        .filter(Ticket.fecha_realizar_servicio < end)
        .order_by(Ticket.fecha_realizar_servicio.asc())
    )

    rows = q.all()
    visits: List[VisitOut] = []
    for t, c in rows:
        visits.append(VisitOut(
            id=t.id,
            client=getattr(c, "name", None),
            address=t.address,
            contact_phone=getattr(c, "phone", None),
            window_from=t.fecha_realizar_servicio,
            window_to=t.fecha_termino_servicio,
            lat=t.latitude,
            lon=t.longitude,
        ))
    return visits
