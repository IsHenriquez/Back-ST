from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.user import User

router = APIRouter()

@router.post("/login")
def login(payload: dict, db: Session = Depends(get_db)):
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        raise HTTPException(400, "email y password requeridos")

    user = db.query(User).filter(User.email == email).first()
    if not user or user.password != password:   
        raise HTTPException(401, "Credenciales inválidas")

    return {"user": {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "id_vehicle": user.id_vehicle
    }}
