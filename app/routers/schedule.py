# routers/schedule.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.ticket import Ticket  # ajusta import si tu ruta difiere

router = APIRouter(prefix="/schedule", tags=["schedule"])

# ----- Límites del día -----
# Usa UTC porque Railway/MySQL normalmente guarda en UTC.
# Si tu BD está en hora local, cambia utcnow() por now().
def day_bounds():
    start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end

@router.get("/today")
def schedule_today(user_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    """
    Visitas de HOY del técnico (solo ACTIVAS):
    - fecha_realizar_servicio ∈ HOY
    - fecha_termino_servicio IS NULL
    - orden por fecha_realizar_servicio
    """
    start, end = day_bounds()

    qs = (
        db.query(Ticket)
        .filter(Ticket.user_id == user_id)
        .filter(Ticket.fecha_realizar_servicio >= start,
                Ticket.fecha_realizar_servicio < end)
        .filter(Ticket.fecha_termino_servicio.is_(None))
        .order_by(Ticket.fecha_realizar_servicio.asc())
    )

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
    Jornada de HOY por técnico (independiente de IDs de estado):
    - Activos hoy     = fecha_realizar_servicio ∈ HOY  y fecha_termino_servicio IS NULL
    - Terminados hoy  = fecha_termino_servicio ∈ HOY
    """
    start, end = day_bounds()

    activos_hoy = db.query(func.count(Ticket.id)) \
        .filter(Ticket.user_id == user_id) \
        .filter(Ticket.fecha_realizar_servicio >= start,
                Ticket.fecha_realizar_servicio < end) \
        .filter(Ticket.fecha_termino_servicio.is_(None)) \
        .scalar() or 0

    terminados_hoy = db.query(func.count(Ticket.id)) \
        .filter(Ticket.user_id == user_id) \
        .filter(Ticket.fecha_termino_servicio >= start,
                Ticket.fecha_termino_servicio < end) \
        .scalar() or 0

    return {
        "assignedToday": int(activos_hoy),     # el front lo muestra como "Activos"
        "resolvedToday": int(terminados_hoy),  # el front lo muestra como "Terminados"
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
    t = (
        db.query(Ticket)
        .filter(Ticket.user_id == user_id)
        .order_by(Ticket.created_at.desc())
        .first()
    )
    if not t:
        return None
    return {
        "id": t.id,
        "title": t.title,
        "summary": (t.description or "")[:140],
        "created_at": t.created_at.isoformat()
    }
