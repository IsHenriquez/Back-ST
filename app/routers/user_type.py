from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user_type import UserType, UserTypeCreate, UserTypeUpdate
from app.crud.user_type import get_user_type, get_user_types, create_user_type, update_user_type, delete_user_type
from app.core.database import get_db

router = APIRouter(
    prefix="/users_type",
    tags=["users_type"]
)

@router.get("/", response_model=List[UserType])
def read_user_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_user_types(db, skip=skip, limit=limit)

@router.post("/", response_model=UserType)
def create_new_user_type(user_type: UserTypeCreate, db: Session = Depends(get_db)):
    return create_user_type(db, user_type)

@router.get("/{user_type_id}", response_model=UserType)
def read_user_type(user_type_id: int, db: Session = Depends(get_db)):
    db_user_type = get_user_type(db, user_type_id)
    if db_user_type is None:
        raise HTTPException(status_code=404, detail="User Type not found")
    return db_user_type

@router.put("/{user_type_id}", response_model=UserType)
def update_existing_user_type(user_type_id: int, user_type: UserTypeUpdate, db: Session = Depends(get_db)):
    db_user_type = update_user_type(db, user_type_id, user_type)
    if db_user_type is None:
        raise HTTPException(status_code=404, detail="User Type not found")
    return db_user_type

@router.delete("/{user_type_id}", response_model=UserType)
def delete_existing_user_type(user_type_id: int, db: Session = Depends(get_db)):
    db_user_type = delete_user_type(db, user_type_id)
    if db_user_type is None:
        raise HTTPException(status_code=404, detail="User Type not found")
    return db_user_type
