from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.tickets_priority import TicketsPriority, TicketsPriorityCreate, TicketsPriorityUpdate
from app.crud.tickets_priority import get_priority, get_priorities, create_priority, update_priority, delete_priority
from app.core.database import get_db

router = APIRouter(
    prefix="/tickets_priority",
    tags=["tickets_priority"]
)

@router.get("/", response_model=List[TicketsPriority])
def read_priorities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_priorities(db, skip=skip, limit=limit)

@router.post("/", response_model=TicketsPriority)
def create_new_priority(priority: TicketsPriorityCreate, db: Session = Depends(get_db)):
    return create_priority(db, priority)

@router.get("/{priority_id}", response_model=TicketsPriority)
def read_priority(priority_id: int, db: Session = Depends(get_db)):
    db_priority = get_priority(db, priority_id)
    if db_priority is None:
        raise HTTPException(status_code=404, detail="Priority not found")
    return db_priority

@router.put("/{priority_id}", response_model=TicketsPriority)
def update_existing_priority(priority_id: int, priority: TicketsPriorityUpdate, db: Session = Depends(get_db)):
    db_priority = update_priority(db, priority_id, priority)
    if db_priority is None:
        raise HTTPException(status_code=404, detail="Priority not found")
    return db_priority

@router.delete("/{priority_id}", response_model=TicketsPriority)
def delete_existing_priority(priority_id: int, db: Session = Depends(get_db)):
    db_priority = delete_priority(db, priority_id)
    if db_priority is None:
        raise HTTPException(status_code=404, detail="Priority not found")
    return db_priority
