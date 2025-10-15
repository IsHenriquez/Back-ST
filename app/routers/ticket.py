# app/routers/ticket.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import urllib.parse
from datetime import datetime

# Schemas y modelos
from app.schemas.ticket import TicketCreate, TicketUpdate, Ticket
from app.schemas.ticket import Ticket as TicketSchema
from app.models.ticket import Ticket as TicketModel

# CRUD existente (se mantiene)
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

router = APIRouter(prefix="/tickets", tags=["tickets"])

# ======================================================
# LISTAR TODOS (con filtro opcional)  -> SE MANTIENE
# ======================================================
@router.get("/", response_model=List[TicketSchema])
def read_tickets(
    skip: int = 0,
    limit: int = 10,
    filter: Optional[str] = Query(None),
    db: Session = Depends(get_db),
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



ID_STATUS_ACTIVO    = 2   
ID_STATUS_TERMINADO = 3   

@router.get("/mine", response_model=List[TicketSchema])
def read_my_tickets(
    user_id: int = Query(..., gt=0),
    # aceptamos active|terminated; mantenemos compat con assigned|resolved
    status: Optional[str] = Query(None, pattern="^(active|terminated|assigned|resolved)$"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista tickets del técnico (user_id).
    - status=active      -> ID_STATUS_ACTIVO
    - status=terminated  -> ID_STATUS_TERMINADO
    Compat:
    - status=assigned -> active
    - status=resolved -> terminated

    Si NO viene status (vista "Todos"), se excluyen los pendientes.
    """
    if status == "assigned":
        status = "active"
    elif status == "resolved":
        status = "terminated"

    q = db.query(TicketModel).where(TicketModel.user_id == user_id)

    if status == "active":
        q = q.where(TicketModel.id_status == ID_STATUS_ACTIVO)
    elif status == "terminated":
        q = q.where(TicketModel.id_status == ID_STATUS_TERMINADO)
    else:
        # "Todos": solo activos + terminados (NO pendientes)
        q = q.where(TicketModel.id_status.in_([ID_STATUS_ACTIVO, ID_STATUS_TERMINADO]))

    return (q.order_by(TicketModel.created_at.desc())
             .offset(skip).limit(limit).all() or [])



@router.put("/{ticket_id}/resolve", response_model=TicketSchema)
def resolve_ticket(ticket_id: int, db: Session = Depends(get_db)):
    obj = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Ticket not found")
    obj.id_status = ID_STATUS_TERMINADO
    if getattr(obj, "fecha_termino_servicio", None) is None:
        obj.fecha_termino_servicio = datetime.utcnow()
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

# ======================================================
# CREAR / OBTENER / ACTUALIZAR / ELIMINAR (existente)
# ======================================================

@router.post("/", response_model=Ticket, status_code=status.HTTP_201_CREATED)
def create_new_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    # Si el front ya manda id_managing_user y user_id, respétalos; si no, aplica defaults
    safe_ticket = ticket.copy(update={
        "id_managing_user": ticket.id_managing_user or ticket.user_id,  # o levanta 400 si quieres forzar
        "user_id": ticket.user_id or ticket.id_managing_user,
        "id_status": ticket.id_status or 1,
        "fecha_realizar_servicio": ticket.fecha_realizar_servicio or datetime.utcnow(),
        "fecha_termino_servicio": None,
    })

    # Validación explícita si ninguna de las dos llegó
    if not safe_ticket.id_managing_user:
        raise HTTPException(status_code=400, detail="id_managing_user requerido")

    obj = create_ticket(db, safe_ticket)  # pasa Pydantic, no dict
    return obj

@router.get("/{ticket_id}", response_model=TicketSchema)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = get_ticket(db, ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.put("/{ticket_id}", response_model=TicketSchema)
def update_existing_ticket(ticket_id: int, ticket: TicketUpdate, db: Session = Depends(get_db)):
    db_ticket = update_ticket(db, ticket_id, ticket)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.delete("/{ticket_id}", response_model=TicketSchema)
def delete_existing_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = delete_ticket(db, ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket
