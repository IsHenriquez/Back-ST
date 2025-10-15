from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.models.announcement import Announcement
from app.schemas.announcement import Announcement, AnnouncementCreate, AnnouncementUpdate
from app.crud.announcement import get_announcement, get_announcements, create_announcement, update_announcement, delete_announcement
from app.core.database import get_db

router = APIRouter(
    prefix="/announcements",
    tags=["announcements"]
)

@router.get("/", response_model=List[Announcement])
def read_announcements(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_announcements(db, skip=skip, limit=limit)

@router.get("")
def list_announcements(limit: int = Query(3, ge=1, le=20), db: Session = Depends(get_db)):
    q = db.query(Announcement).order_by(Announcement.created_at.desc()).limit(limit)
    return q.all() or []

@router.post("/", response_model=Announcement)
def create_new_announcement(announcement: AnnouncementCreate, db: Session = Depends(get_db)):
    return create_announcement(db, announcement)

@router.get("/{announcement_id}", response_model=Announcement)
def read_announcement(announcement_id: int, db: Session = Depends(get_db)):
    db_announcement = get_announcement(db, announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return db_announcement

@router.put("/{announcement_id}", response_model=Announcement)
def update_existing_announcement(announcement_id: int, announcement: AnnouncementUpdate, db: Session = Depends(get_db)):
    db_announcement = update_announcement(db, announcement_id, announcement)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return db_announcement

@router.delete("/{announcement_id}", response_model=Announcement)
def delete_existing_announcement(announcement_id: int, db: Session = Depends(get_db)):
    db_announcement = delete_announcement(db, announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return db_announcement
