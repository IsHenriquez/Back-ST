from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnnouncementBase(BaseModel):
    id_announcement_user: Optional[int] = None
    title: str
    description: Optional[str] = None

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(AnnouncementBase):
    pass

class AnnouncementInDBBase(AnnouncementBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Announcement(AnnouncementInDBBase):
    pass
