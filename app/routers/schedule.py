# routers/schedule.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.ticket import Ticket  # ajusta import al tuyo

router = APIRouter(prefix="/schedule", tags=["schedule"])

def today_bounds_utc(now: datetime):
    start = datetime(now.year, now.month, now.day, 0, 0, 0)
    end = start + timedelta(days=1)
    return start, end

@router.get("/today")
def schedule_today(
    user_id: int = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    """
    Visitas de HOY del técnico (tickets NO resueltos),
    ordenados por fecha_realizar_servicio asc.
    """
    now = datetime.utcnow()
    start, end = today_bounds_utc(now)

    qs = (db.query(Ticket)
            .filter(Ticket.user_id == user_id)
            .filter(Ticket.fecha_realizar_servicio >= start,
                    Ticket.fecha_realizar_servicio < end)
            .filter(Ticket.fecha_termino_servicio.is_(None))  # <- EXCLUYE resueltos
            .order_by(Ticket.fecha_realizar_servicio.asc()))

    return [{
        "id": t.id,
        "address": t.address or "",
        "window_from": (t.fecha_realizar_servicio or t.created_at).isoformat(),
        "window_to": (t.fecha_termino_servicio or t.fecha_realizar_servicio or t.created_at).isoformat(),
        "lat": t.latitude,
        "lon": t.longitude
    } for t in qs.all()]

@router.get("/summary/today")
def schedule_summary_today(
    user_id: int = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    """
    Jornada de HOY por técnico:
    - assignedToday: tickets con ventana de servicio HOY
    - resolvedToday: tickets terminados HOY
    - pendingToday: assignedToday - resolvedToday (>=0)
    """
    now = datetime.utcnow()
    start, end = today_bounds_utc(now)

    assigned = db.query(func.count(Ticket.id))\
        .filter(Ticket.user_id == user_id)\
        .filter(Ticket.fecha_realizar_servicio >= start,
                Ticket.fecha_realizar_servicio < end)\
        .scalar() or 0

    resolved = db.query(func.count(Ticket.id))\
        .filter(Ticket.user_id == user_id)\
        .filter(Ticket.fecha_termino_servicio >= start,
                Ticket.fecha_termino_servicio < end)\
        .scalar() or 0

    pending = assigned - resolved
    if pending < 0:
        pending = 0

    return {
        "assignedToday": int(assigned),
        "resolvedToday": int(resolved),
        "pendingToday": int(pending)
    }

@router.get("/last")
def schedule_last(
    user_id: int = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    """
    Último ticket del técnico (por created_at).
    """
    t = (db.query(Ticket)
            .filter(Ticket.user_id == user_id)
            .order_by(Ticket.created_at.desc())
            .first())
    if not t:
        return None
    return {
        "id": t.id,
        "title": t.title,
        "summary": (t.description or "")[:140],
        "created_at": t.created_at.isoformat()
    }
