# routers/schedule.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.ticket import Ticket  # ajusta import al tuyo

router = APIRouter(prefix="/schedule", tags=["schedule"])

def day_bounds_local(now: datetime):
    # Usa hora LOCAL del servidor; si tu BD guarda UTC, cambia a datetime.utcnow()
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end

def today_bounds_utc(now: datetime):
    start = datetime(now.year, now.month, now.day, 0, 0, 0)
    end = start + timedelta(days=1)
    return start, end

@router.get("/today")
def schedule_today(user_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    """
    Visitas de HOY del técnico: SOLO tickets ACTIVO (id_status=2)
    con fecha_realizar_servicio dentro de HOY, ordenados por esa fecha.
    """
    start, end = day_bounds_local(datetime.now())

    qs = (db.query(Ticket)
            .filter(Ticket.user_id == user_id)
            .filter(Ticket.id_status == ID_STATUS_ACTIVO)
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

@router.get("/summary/today")
def schedule_summary_today(user_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    """
    Jornada de HOY por técnico:
    - assignedToday := ACTIVO hoy (id_status=2 & fecha_realizar_servicio ∈ HOY)
    - resolvedToday := TERMINADO hoy (id_status=3 & fecha_termino_servicio ∈ HOY)
    - pendingToday  := max(assignedToday - resolvedToday, 0)  (si aún muestras 'pendiente' visual)
    """
    start, end = day_bounds_local(datetime.now())

    activos_hoy = db.query(func.count(Ticket.id))\
        .filter(Ticket.user_id == user_id)\
        .filter(Ticket.id_status == ID_STATUS_ACTIVO)\
        .filter(Ticket.fecha_realizar_servicio >= start,
                Ticket.fecha_realizar_servicio < end)\
        .scalar() or 0

    terminados_hoy = db.query(func.count(Ticket.id))\
        .filter(Ticket.user_id == user_id)\
        .filter(Ticket.id_status == ID_STATUS_TERMINADO)\
        .filter(Ticket.fecha_termino_servicio >= start,
                Ticket.fecha_termino_servicio < end)\
        .scalar() or 0

    # Mantengo las CLAVES esperadas por el front (aunque el UI diga "Activos/Terminados")
    return {
        "assignedToday": int(activos_hoy),    # → se muestra como "Activos"
        "resolvedToday": int(terminados_hoy), # → se muestra como "Terminados"
        "pendingToday":  max(int(activos_hoy) - int(terminados_hoy), 0)
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
