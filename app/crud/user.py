from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    # Temporalmente sin hashear, solo para prueba
    raw_password = user.password[:72]  # Puede omitirlo también
    # hashed_password = pwd_context.hash(raw_password)
    db_user = User(**user.dict(exclude={"password"}), password=raw_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        user_data = user.dict(exclude_unset=True)
        if "password" in user_data and user_data["password"] is not None:
            user_data["password"] = pwd_context.hash(user_data["password"])
        for key, value in user_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
