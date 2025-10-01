from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    name: str
    last_name: Optional[str] = None
    mother_last_name: Optional[str] = None
    identification_number: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerInDBBase(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Customer(CustomerInDBBase):
    pass
