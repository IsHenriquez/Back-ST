# routers/schedule.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.ticket import Ticket  # ajusta import al tuyo

router = APIRouter(prefix="/schedule", tags=["schedule"])

def day_bounds_utc(dt: datetime):
    start = datetime(dt.year, dt.month, dt.day, 0, 0, 0)
    end = start + timedelta(days=1)
    return start, end

@router.get("/summary/today")
def schedule_summary_today(
    user_id: int = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    now = datetime.utcnow()
    start, end = day_bounds_utc(now)

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

    pending = max(assigned - resolved, 0)

    return {
        "assignedToday": int(assigned),
        "resolvedToday": int(resolved),
        "pendingToday": int(pending)
    }
