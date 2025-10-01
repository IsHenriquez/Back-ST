from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserTypeBase(BaseModel):
    name: str
    description: Optional[str] = None

class UserTypeCreate(UserTypeBase):
    pass

class UserTypeUpdate(UserTypeBase):
    pass

class UserTypeInDBBase(UserTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserType(UserTypeInDBBase):
    pass
