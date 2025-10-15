# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.crud.user import get_user_by_email
from app.core.security import verify_password, create_access_token, decode_access_token
from app.core.database import get_db
from app.schemas.user import UserResponse

router = APIRouter()
security = HTTPBearer()

@router.post("/auth/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {
        "user": UserResponse.from_orm(user),
        "token": token,
        "token_type": "Bearer",
        "success": True,
        "tipo_usuario": user.id_user_type
    }

@router.post("/auth/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Por ahora, simplemente responde éxito (para JWT)
    return {"message": "Logged out successfully"}

@router.post("/auth/refresh")
def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    email = payload.get("sub")
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    new_token = create_access_token({"sub": user.email})

    return {
        "user": UserResponse.from_orm(user),
        "token": new_token,
        "token_type": "Bearer",
        "success": True,
        "tipo_usuario": user.id_user_type
    }
