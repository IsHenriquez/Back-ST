from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.ticket_type import TicketType, TicketTypeCreate, TicketTypeUpdate
from app.crud.ticket_type import get_type, get_types, create_type, update_type, delete_type
from app.core.database import get_db

router = APIRouter(
    prefix="/tickets_type",
    tags=["tickets_type"]
)

@router.get("/", response_model=List[TicketType])
def read_types(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_types(db, skip=skip, limit=limit)

@router.post("/", response_model=TicketType)
def create_new_type(type: TicketTypeCreate, db: Session = Depends(get_db)):
    return create_type(db, type)

@router.get("/{type_id}", response_model=TicketType)
def read_type(type_id: int, db: Session = Depends(get_db)):
    db_type = get_type(db, type_id)
    if db_type is None:
        raise HTTPException(status_code=404, detail="Type not found")
    return db_type

@router.put("/{type_id}", response_model=TicketType)
def update_existing_type(type_id: int, type: TicketTypeUpdate, db: Session = Depends(get_db)):
    db_type = update_type(db, type_id, type)
    if db_type is None:
        raise HTTPException(status_code=404, detail="Type not found")
    return db_type

@router.delete("/{type_id}", response_model=TicketType)
def delete_existing_type(type_id: int, db: Session = Depends(get_db)):
    db_type = delete_type(db, type_id)
    if db_type is None:
        raise HTTPException(status_code=404, detail="Type not found")
    return db_type
