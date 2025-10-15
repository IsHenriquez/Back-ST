from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import urllib.parse
from datetime import datetime

# Schemas y modelos
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.schemas.ticket import Ticket as TicketSchema
from app.models.ticket import Ticket as TicketModel

# CRUD existente (lo sigues usando tal cual)
from app.crud.ticket import (
    get_ticket,
    get_tickets,
    get_tickets_with_filter,
    create_ticket,
    update_ticket,
    delete_ticket,
    parse_filter_param
)
from app.core.database import get_db

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)

# ---- LISTAR TODOS (con filtro opcional) ----
@router.get("/", response_model=List[TicketSchema])  # <- TicketSchema
def read_tickets(
    skip: int = 0,
    limit: int = 10,
    filter: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    if filter is not None:
        print("RAW filter recibido:", repr(filter))
        filters = parse_filter_param(filter)
        print("Parsed filters:", filters)
        if filters is None:
            raise HTTPException(status_code=400, detail="Formato de filtro inválido")
        tickets = get_tickets_with_filter(db, filters, skip=skip, limit=limit)
        return tickets or []
    return get_tickets(db, skip=skip, limit=limit) or []

# ---- CREAR ----
@router.post("/", response_model=TicketSchema)  # <- TicketSchema
def create_new_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """
    Normaliza ticket de creación:
    - fecha_realizar_servicio: si no viene, usa ahora (UTC)
    - fecha_termino_servicio: siempre None al crear
    """
    safe_payload = ticket.copy(update={
        "fecha_realizar_servicio": ticket.fecha_realizar_servicio or datetime.utcnow(),
        "fecha_termino_servicio": None,
    })
    return create_ticket(db, safe_payload)

# ---- OBTENER POR ID ----
@router.get("/{ticket_id}", response_model=TicketSchema)  # <- TicketSchema
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = get_ticket(db, ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

# ---- ACTUALIZAR ----
@router.put("/{ticket_id}", response_model=TicketSchema)  # <- TicketSchema
def update_existing_ticket(ticket_id: int, ticket: TicketUpdate, db: Session = Depends(get_db)):
    db_ticket = update_ticket(db, ticket_id, ticket)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

# ---- ELIMINAR ----
@router.delete("/{ticket_id}", response_model=TicketSchema)  # <- TicketSchema
def delete_existing_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = delete_ticket(db, ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


ID_STATUS_PENDIENTE = 1   
ID_STATUS_ACTIVO    = 2   
ID_STATUS_TERMINADO = 3   

@router.get("/mine", response_model=List[TicketSchema])
def read_my_tickets(
    user_id: int = Query(..., gt=0),
    status: Optional[str] = Query(None, regex="^(assigned|pending|resolved)$"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista tickets del técnico. Filtro opcional por estado:
    - assigned -> ID_STATUS_PENDIENTE   (según tus nombres actuales)
    - pending  -> ID_STATUS_ACTIVO
    - resolved -> ID_STATUS_TERMINADO
    """
    q = db.query(TicketModel).where(TicketModel.user_id == user_id)

    if status == "assigned":
        q = q.where(TicketModel.id_status == ID_STATUS_PENDIENTE)
    elif status == "pending":
        q = q.where(TicketModel.id_status == ID_STATUS_ACTIVO)
    elif status == "resolved":
        q = q.where(TicketModel.id_status == ID_STATUS_TERMINADO)

    return q.order_by(TicketModel.created_at.desc()).offset(skip).limit(limit).all() or []

@router.put("/{ticket_id}/resolve", response_model=TicketSchema)
def resolve_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """
    Marca ticket como TERMINADO y setea fecha_termino_servicio si está NULL.
    """
    obj = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Ticket not found")

    obj.id_status = ID_STATUS_TERMINADO  # <- antes usabas ID_STATUS_RESUELTO (no existe)
    if getattr(obj, "fecha_termino_servicio", None) is None:
        obj.fecha_termino_servicio = datetime.utcnow()

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
