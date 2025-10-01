from sqlalchemy.orm import Session
from app.models.tickets_priority import TicketsPriority
from app.schemas.tickets_priority import TicketsPriorityCreate, TicketsPriorityUpdate

def get_priority(db: Session, priority_id: int):
    return db.query(TicketsPriority).filter(TicketsPriority.id == priority_id).first()

def get_priorities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TicketsPriority).offset(skip).limit(limit).all()

def create_priority(db: Session, priority: TicketsPriorityCreate):
    db_priority = TicketsPriority(**priority.dict())
    db.add(db_priority)
    db.commit()
    db.refresh(db_priority)
    return db_priority

def update_priority(db: Session, priority_id: int, priority: TicketsPriorityUpdate):
    db_priority = db.query(TicketsPriority).filter(TicketsPriority.id == priority_id).first()
    if db_priority:
        for key, value in priority.dict(exclude_unset=True).items():
            setattr(db_priority, key, value)
        db.commit()
        db.refresh(db_priority)
    return db_priority

def delete_priority(db: Session, priority_id: int):
    db_priority = db.query(TicketsPriority).filter(TicketsPriority.id == priority_id).first()
    if db_priority:
        db.delete(db_priority)
        db.commit()
    return db_priority
