from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.ticket import Ticket, TicketCreate, TicketUpdate
from app.crud.ticket import get_ticket, get_tickets, create_ticket, update_ticket, delete_ticket
from app.core.database import get_db

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)

@router.get("/", response_model=List[Ticket])
def read_tickets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_tickets(db, skip=skip, limit=limit)

@router.post("/", response_model=Ticket)
def create_new_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    return create_ticket(db, ticket)

@router.get("/{ticket_id}", response_model=Ticket)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = get_ticket(db, ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.put("/{ticket_id}", response_model=Ticket)
def update_existing_ticket(ticket_id: int, ticket: TicketUpdate, db: Session = Depends(get_db)):
    db_ticket = update_ticket(db, ticket_id, ticket)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.delete("/{ticket_id}", response_model=Ticket)
def delete_existing_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = delete_ticket(db, ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket
