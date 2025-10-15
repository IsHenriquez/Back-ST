# routers/schedule.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.ticket import Ticket  # ajusta import al tuyo

router = APIRouter(prefix="/schedule", tags=["schedule"])

@router.get("/today")
def schedule_today(user_id: int = Query(...), db: Session = Depends(get_db)):
    start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    qs = (db.query(Ticket)
            .filter(Ticket.user_id == user_id)
            .filter(Ticket.fecha_realizar_servicio >= start,
                    Ticket.fecha_realizar_servicio < end)
            .order_by(Ticket.fecha_realizar_servicio.asc()))
    return [{
        "id": t.id,
        "address": t.address or "",
        "window_from": (t.fecha_realizar_servicio or t.created_at).isoformat(),
        "window_to": (t.fecha_termino_servicio or t.fecha_realizar_servicio or t.created_at).isoformat(),
        "lat": t.latitude,
        "lon": t.longitude
    } for t in qs.all()]
