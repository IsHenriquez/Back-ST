from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.db import get_db
from app.models.ticket import Ticket

router = APIRouter()

@router.get("/today")
def visits_today(user_id: int, db: Session = Depends(get_db)):
    # rango del día 
    today = datetime.now().date()
    start = datetime.combine(today, datetime.min.time())
    end   = datetime.combine(today, datetime.max.time())

    q = (db.query(Ticket)
           .filter(Ticket.id_managing_user == user_id)
           .filter(Ticket.fecha_realizar_servicio >= start)
           .filter(Ticket.fecha_realizar_servicio <= end)
           .order_by(Ticket.fecha_realizar_servicio.asc()))
    items = []
    for t in q.all():
        items.append({
            "id": t.id,
            "client": "", 
            "address": t.address,
            "window_from": t.fecha_realizar_servicio.isoformat() if t.fecha_realizar_servicio else None,
            "window_to":   t.fecha_realizar_servicio.isoformat() if t.fecha_realizar_servicio else None,
            "lat": t.latitude, "lon": t.longitude,
            "contact_phone": None
        })
    return items

@router.get("/summary/today")
def summary_today(user_id: int, db: Session = Depends(get_db)):
    today = datetime.now().date()
    start = datetime.combine(today, datetime.min.time())
    end   = datetime.combine(today, datetime.max.time())

    base = db.query(Ticket).filter(Ticket.id_managing_user == user_id)\
                           .filter(Ticket.fecha_realizar_servicio >= start)\
                           .filter(Ticket.fecha_realizar_servicio <= end)
    total = base.count()
    resolved = base.filter(Ticket.id_status.in_([/* id resolved/closed */])).count()
    pending  = total - resolved
    return {"assignedToday": total, "resolvedToday": resolved, "pendingToday": pending}

@router.get("/last")
def last_ticket(user_id: int, db: Session = Depends(get_db)):
    t = (db.query(Ticket)
           .filter(Ticket.id_managing_user == user_id)
           .order_by(Ticket.id.desc())  
           .first())
    if not t:
        return None
    return {
        "id": t.id,
        "title": (t.title or "")[:80],
        "summary": (t.description or "")[:200],
        "created_at": t.fecha_realizar_servicio.isoformat() if t.fecha_realizar_servicio else None
    }
