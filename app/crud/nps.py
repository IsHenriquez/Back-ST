from sqlalchemy.orm import Session
from app.models.nps import NPS
from app.schemas.nps import NPSCreate, NPSUpdate

def get_nps(db: Session, nps_id: int):
    return db.query(NPS).filter(NPS.id == nps_id).first()

def get_all_nps(db: Session, skip: int = 0, limit: int = 100):
    return db.query(NPS).offset(skip).limit(limit).all()

def create_nps(db: Session, nps: NPSCreate):
    db_nps = NPS(**nps.dict())
    db.add(db_nps)
    db.commit()
    db.refresh(db_nps)
    return db_nps

def update_nps(db: Session, nps_id: int, nps: NPSUpdate):
    db_nps = db.query(NPS).filter(NPS.id == nps_id).first()
    if db_nps:
        for key, value in nps.dict(exclude_unset=True).items():
            setattr(db_nps, key, value)
        db.commit()
        db.refresh(db_nps)
    return db_nps

def delete_nps(db: Session, nps_id: int):
    db_nps = db.query(NPS).filter(NPS.id == nps_id).first()
    if db_nps:
        db.delete(db_nps)
        db.commit()
    return db_nps
