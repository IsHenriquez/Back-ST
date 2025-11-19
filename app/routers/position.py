from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.position import Position, PositionCreate
from app.crud.position import get_all_positions, get_position, create_position, update_position, delete_position
from app.core.database import get_db

router = APIRouter(
    prefix="/position",
    tags=["position"]
)

@router.get("/", response_model=List[Position])
def read_positions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_positions(db, skip=skip, limit=limit)

@router.get("/{position_id}", response_model=Position)
def read_position_by_id(position_id: int, db: Session = Depends(get_db)):
    db_position = get_position(db, position_id)
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return db_position

@router.post("/", response_model=Position)
def create_new_position(position: PositionCreate, db: Session = Depends(get_db)):
    return create_position(db, position)

@router.put("/{position_id}", response_model=Position)
def update_existing_position(position_id: int, position: PositionCreate, db: Session = Depends(get_db)):
    db_position = update_position(db, position_id, position)
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return db_position

@router.delete("/{position_id}", response_model=Position)
def delete_existing_position(position_id: int, db: Session = Depends(get_db)):
    db_position = delete_position(db, position_id)
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return db_position

