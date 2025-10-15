# app/schemas/user_type.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserTypeBase(BaseModel):
    name: str
    description: Optional[str] = None

class UserTypeCreate(UserTypeBase):
    pass

class UserTypeUpdate(UserTypeBase):
    name: Optional[str] = None

class UserType(UserTypeBase):
    id: int
    created_at: Optional[datetime] = None  # <-- Haz esto opcional
    updated_at: Optional[datetime] = None  # <-- Haz esto opcional
    
    class Config:
        from_attributes = True
