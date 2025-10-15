# app/routers/ticket.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import urllib.parse
from datetime import datetime

# Schemas y modelos
from app.schemas.ticket import TicketCreate, TicketUpdate
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

# ======================================================
# Mis tickets (por técnico) + resolver
# PUESTO ANTES de rutas dinámicas para evitar 422
# ======================================================

# AJUSTA estos IDs a los reales en tu tabla tickets_status
ID_STATUS_PENDIENTE = 1   # "Pendiente/Asignado" según su uso actual
ID_STATUS_ACTIVO    = 2   # "En curso/Activo"
ID_STATUS_TERMINADO = 3   # "Terminado/Resuelto"

@router.get("/mine", response_model=List[TicketSchema])
def read_my_tickets(
    user_id: int = Query(..., gt=0),
    # En Pydantic v2 usar "pattern"; si usas v1, cambia a "regex"
    status: Optional[str] = Query(None, pattern="^(assigned|pending|resolved)$"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista tickets del técnico (user_id). Filtro opcional por estado:
    - status=assigned -> ID_STATUS_PENDIENTE
    - status=pending  -> ID_STATUS_ACTIVO
    - status=resolved -> ID_STATUS_TERMINADO
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

    obj.id_status = ID_STATUS_TERMINADO
    if getattr(obj, "fecha_termino_servicio", None) is None:
        obj.fecha_termino_servicio = datetime.utcnow()

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# ======================================================
# CREAR / OBTENER / ACTUALIZAR / ELIMINAR (existente)
# ======================================================

@router.post("/", response_model=TicketModel, status_code=status.HTTP_201_CREATED)
def create_new_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
):
    vals = ticket.model_dump(exclude_unset=True)

    # Si front ya los manda, no los toques; si faltan, aplica fallback seguro:
    if vals.get("id_managing_user") is None:
        # último recurso: usa user_id si vino
        if vals.get("user_id") is not None:
            vals["id_managing_user"] = vals["user_id"]
        else:
            raise HTTPException(status_code=400, detail="id_managing_user requerido")

    if vals.get("user_id") is None:
        # si tu modelo exige user_id, usa el mismo manager como solicitante
        vals["user_id"] = vals["id_managing_user"]

    vals.setdefault("id_status", 1)
    vals.setdefault("fecha_realizar_servicio", datetime.utcnow())
    vals["fecha_termino_servicio"] = None

    obj = create_ticket(db, vals)
    if not obj:
        raise HTTPException(status_code=400, detail="No se pudo crear el ticket")
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
