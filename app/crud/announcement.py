from sqlalchemy.orm import Session
from app.models.announcement import Announcement
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate

def get_announcement(db: Session, announcement_id: int):
    return db.query(Announcement).filter(Announcement.id == announcement_id).first()

def get_announcements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Announcement).offset(skip).limit(limit).all()

def create_announcement(db: Session, announcement: AnnouncementCreate):
    db_announcement = Announcement(**announcement.dict())
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

def update_announcement(db: Session, announcement_id: int, announcement: AnnouncementUpdate):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if db_announcement:
        for key, value in announcement.dict(exclude_unset=True).items():
            setattr(db_announcement, key, value)
        db.commit()
        db.refresh(db_announcement)
    return db_announcement

def delete_announcement(db: Session, announcement_id: int):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if db_announcement:
        db.delete(db_announcement)
        db.commit()
    return db_announcement
