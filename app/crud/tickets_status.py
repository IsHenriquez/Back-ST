from sqlalchemy.orm import Session
from app.models.tickets_status import TicketsStatus
from app.schemas.tickets_status import TicketsStatusCreate, TicketsStatusUpdate

def get_status(db: Session, status_id: int):
    return db.query(TicketsStatus).filter(TicketsStatus.id == status_id).first()

def get_statuses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TicketsStatus).offset(skip).limit(limit).all()

def create_status(db: Session, status: TicketsStatusCreate):
    db_status = TicketsStatus(**status.dict())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

def update_status(db: Session, status_id: int, status: TicketsStatusUpdate):
    db_status = db.query(TicketsStatus).filter(TicketsStatus.id == status_id).first()
    if db_status:
        for key, value in status.dict(exclude_unset=True).items():
            setattr(db_status, key, value)
        db.commit()
        db.refresh(db_status)
    return db_status

def delete_status(db: Session, status_id: int):
    db_status = db.query(TicketsStatus).filter(TicketsStatus.id == status_id).first()
    if db_status:
        db.delete(db_status)
        db.commit()
    return db_status
