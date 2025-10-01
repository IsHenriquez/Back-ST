from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.tickets_status import TicketsStatus, TicketsStatusCreate, TicketsStatusUpdate
from app.crud.tickets_status import get_status, get_statuses, create_status, update_status, delete_status
from app.core.database import get_db

router = APIRouter(
    prefix="/tickets_status",
    tags=["tickets_status"]
)

@router.get("/", response_model=List[TicketsStatus])
def read_statuses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_statuses(db, skip=skip, limit=limit)

@router.post("/", response_model=TicketsStatus)
def create_new_status(status: TicketsStatusCreate, db: Session = Depends(get_db)):
    return create_status(db, status)

@router.get("/{status_id}", response_model=TicketsStatus)
def read_status(status_id: int, db: Session = Depends(get_db)):
    db_status = get_status(db, status_id)
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return db_status

@router.put("/{status_id}", response_model=TicketsStatus)
def update_existing_status(status_id: int, status: TicketsStatusUpdate, db: Session = Depends(get_db)):
    db_status = update_status(db, status_id, status)
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return db_status

@router.delete("/{status_id}", response_model=TicketsStatus)
def delete_existing_status(status_id: int, db: Session = Depends(get_db)):
    db_status = delete_status(db, status_id)
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return db_status
