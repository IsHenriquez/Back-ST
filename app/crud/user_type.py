from sqlalchemy.orm import Session
from app.models.user_type import UserType
from app.schemas.user_type import UserTypeCreate, UserTypeUpdate

def get_user_type(db: Session, user_type_id: int):
    return db.query(UserType).filter(UserType.id == user_type_id).first()

def get_user_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserType).offset(skip).limit(limit).all()

def create_user_type(db: Session, user_type: UserTypeCreate):
    db_user_type = UserType(**user_type.dict())
    db.add(db_user_type)
    db.commit()
    db.refresh(db_user_type)
    return db_user_type

def update_user_type(db: Session, user_type_id: int, user_type: UserTypeUpdate):
    db_user_type = db.query(UserType).filter(UserType.id == user_type_id).first()
    if db_user_type:
        for key, value in user_type.dict(exclude_unset=True).items():
            setattr(db_user_type, key, value)
        db.commit()
        db.refresh(db_user_type)
    return db_user_type

def delete_user_type(db: Session, user_type_id: int):
    db_user_type = db.query(UserType).filter(UserType.id == user_type_id).first()
    if db_user_type:
        db.delete(db_user_type)
        db.commit()
    return db_user_type
