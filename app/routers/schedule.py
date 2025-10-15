# routers/schedule.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.ticket import Ticket

router = APIRouter(prefix="/schedule", tags=["schedule"])

ID_STATUS_ACTIVO    = 2
ID_STATUS_TERMINADO = 3

def day_bounds_local():
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end

@router.get("/today")
def schedule_today(user_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    """
    HOY (local):
      - id_status = ACTIVO
      - fecha base = COALESCE(fecha_realizar_servicio, created_at)
      - excluye terminados
    """
    start, end = day_bounds_local()
    base_dt = func.coalesce(Ticket.fecha_realizar_servicio, Ticket.created_at)

    qs = (db.query(Ticket)
            .filter(Ticket.user_id == user_id)
            .filter(Ticket.id_status == ID_STATUS_ACTIVO)
            .filter(Ticket.fecha_termino_servicio.is_(None))
            .filter(base_dt >= start, base_dt < end)
            .order_by(base_dt.asc()))

    return [{
        "id": t.id,
        "address": t.address or "",
        "window_from": (t.fecha_realizar_servicio or t.created_at).isoformat(),
        "window_to": (t.fecha_termino_servicio or t.fecha_realizar_servicio or t.created_at).isoformat(),
        "lat": t.latitude,
        "lon": t.longitude
    } for t in qs.all()]

@router.get("/summary/today")
def schedule_summary_today(user_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    """
    Jornada HOY (local):
      - Activos  := id_status=2 AND base_dt ∈ HOY AND no terminados
      - Terminados := id_status=3 AND fecha_termino_servicio ∈ HOY
    """
    start, end = day_bounds_local()
    base_dt = func.coalesce(Ticket.fecha_realizar_servicio, Ticket.created_at)

    activos_hoy = db.query(func.count(Ticket.id))\
        .filter(Ticket.user_id == user_id)\
        .filter(Ticket.id_status == ID_STATUS_ACTIVO)\
        .filter(Ticket.fecha_termino_servicio.is_(None))\
        .filter(base_dt >= start, base_dt < end)\
        .scalar() or 0

    terminados_hoy = db.query(func.count(Ticket.id))\
        .filter(Ticket.user_id == user_id)\
        .filter(Ticket.id_status == ID_STATUS_TERMINADO)\
        .filter(Ticket.fecha_termino_servicio >= start,
                Ticket.fecha_termino_servicio < end)\
        .scalar() or 0

    return {
        "assignedToday": int(activos_hoy),
        "resolvedToday": int(terminados_hoy),
        "pendingToday":  max(int(activos_hoy) - int(terminados_hoy), 0)
    }

@router.get("/last")
def schedule_last(user_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
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
