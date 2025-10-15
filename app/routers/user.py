# app/routers/user.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.user import get_users, create_user, update_user, delete_user, get_user
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.utils.password_generator import generate_password_from_user_data

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    u = get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(payload: UserCreate, db: Session = Depends(get_db)):
    # Convertir a dict para manipular
    vals = payload.model_dump(exclude_unset=True)
    
    # Generar password si no viene
    if not vals.get("password"):
        password = generate_password_from_user_data(
            name=vals.get("name", ""),
            last_name=vals.get("last_name", ""),
            identification=vals.get("identification_number", "")
        )
        vals["password"] = password
        print(f"[User Create] Password generado: {password}")
    
    # Crear usuario con el dict actualizado
    # Convertir de nuevo a UserCreate para pasar al CRUD
    payload_with_password = UserCreate(**vals)
    return create_user(db, payload_with_password)


@router.put("/{user_id}", response_model=UserOut)
def update_user_endpoint(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    u = update_user(db, user_id, payload)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    ok = delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return None
