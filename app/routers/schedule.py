# routers/schedule.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.ticket import Ticket  # ajusta import si tu ruta difiere

router = APIRouter(prefix="/schedule", tags=["schedule"])

# ====== IDs de estado (ajusta si tus valores son otros) ======
ID_STATUS_ACTIVO    = 2   # tickets asignados/activos para el técnico
ID_STATUS_TERMINADO = 3   # tickets resueltos/terminados

# ====== Día de HOY (HORA LOCAL). Si tu BD guarda UTC, cambia now() por utcnow() ======
def day_bounds_local():
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end

@router.get("/today")
def schedule_today(user_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    """
    Visitas de HOY del técnico:
    - SOLO tickets Activos (id_status = ID_STATUS_ACTIVO)
    - fecha_realizar_servicio dentro de HOY (local)
    - EXCLUYE terminados (fecha_termino_servicio IS NULL)
    - Ordenados por fecha_realizar_servicio
    """
    start, end = day_bounds_local()

    qs = (
        db.query(Ticket)
        .filter(Ticket.user_id == user_id)
        .filter(Ticket.id_status == ID_STATUS_ACTIVO)
        .filter(Ticket.fecha_termino_servicio.is_(None))
        .filter(Ticket.fecha_realizar_servicio >= start,
                Ticket.fecha_realizar_servicio < end)
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
    Jornada de HOY por técnico (local):
    - Activos hoy     := id_status = ACTIVO  AND fecha_realizar_servicio ∈ HOY AND fecha_termino_servicio IS NULL
    - Terminados hoy  := id_status = TERMINADO AND fecha_termino_servicio ∈ HOY
    """
    start, end = day_bounds_local()

    activos_hoy = db.query(func.count(Ticket.id)) \
        .filter(Ticket.user_id == user_id) \
        .filter(Ticket.id_status == ID_STATUS_ACTIVO) \
        .filter(Ticket.fecha_termino_servicio.is_(None)) \
        .filter(Ticket.fecha_realizar_servicio >= start,
                Ticket.fecha_realizar_servicio < end) \
        .scalar() or 0

    terminados_hoy = db.query(func.count(Ticket.id)) \
        .filter(Ticket.user_id == user_id) \
        .filter(Ticket.id_status == ID_STATUS_TERMINADO) \
        .filter(Ticket.fecha_termino_servicio >= start,
                Ticket.fecha_termino_servicio < end) \
        .scalar() or 0

    # El front usa estas claves; en UI se muestran como "Activos" y "Terminados"
    return {
        "assignedToday": int(activos_hoy),
        "resolvedToday": int(terminados_hoy),
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
