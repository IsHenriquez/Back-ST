from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import date, datetime

class UserBase(BaseModel):
    name: str
    last_name: Optional[str] = None
    mother_last_name: Optional[str] = None
    identification_number: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    active: Optional[bool] = True
    id_user_type: int

class UserCreate(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    identification_number: Optional[str] = None
    id_user_type: int
    active: Optional[bool] = True
    password: Optional[str] = None  # <-- Opcional

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    email_verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    id_user_type: int

    model_config = {
        "from_attributes": True
    }


class UserOut(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class User(UserInDBBase):
    pass
