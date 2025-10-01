from sqlalchemy.orm import Session
from app.models.ticket_type import TicketType
from app.schemas.ticket_type import TicketTypeCreate, TicketTypeUpdate

def get_type(db: Session, type_id: int):
    return db.query(TicketType).filter(TicketType.id == type_id).first()

def get_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TicketType).offset(skip).limit(limit).all()

def create_type(db: Session, type: TicketTypeCreate):
    db_type = TicketType(**type.dict())
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type

def update_type(db: Session, type_id: int, type: TicketTypeUpdate):
    db_type = db.query(TicketType).filter(TicketType.id == type_id).first()
    if db_type:
        for key, value in type.dict(exclude_unset=True).items():
            setattr(db_type, key, value)
        db.commit()
        db.refresh(db_type)
    return db_type

def delete_type(db: Session, type_id: int):
    db_type = db.query(TicketType).filter(TicketType.id == type_id).first()
    if db_type:
        db.delete(db_type)
        db.commit()
    return db_type
