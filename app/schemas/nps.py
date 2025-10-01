from pydantic import BaseModel

class NPSBase(BaseModel):
    id_user: int
    id_customer: int
    id_ticket: int
    evaluation: int

class NPSCreate(NPSBase):
    pass

class NPSUpdate(NPSBase):
    pass

class NPSInDBBase(NPSBase):
    id: int

    class Config:
        orm_mode = True

class NPS(NPSInDBBase):
    pass
