from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.ticket_category import TicketCategory, TicketCategoryCreate, TicketCategoryUpdate
from app.crud.ticket_category import get_category, get_categories, create_category, update_category, delete_category
from app.core.database import get_db

router = APIRouter(
    prefix="/tickets_category",
    tags=["tickets_category"]
)

@router.get("/", response_model=List[TicketCategory])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_categories(db, skip=skip, limit=limit)

@router.post("/", response_model=TicketCategory)
def create_new_category(category: TicketCategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category)

@router.get("/{category_id}", response_model=TicketCategory)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put("/{category_id}", response_model=TicketCategory)
def update_existing_category(category_id: int, category: TicketCategoryUpdate, db: Session = Depends(get_db)):
    db_category = update_category(db, category_id, category)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/{category_id}", response_model=TicketCategory)
def delete_existing_category(category_id: int, db: Session = Depends(get_db)):
    db_category = delete_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category
