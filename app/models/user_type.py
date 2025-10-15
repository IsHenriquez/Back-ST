# app/models/user_type.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserType(Base):
    __tablename__ = "user_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    users = relationship("User", back_populates="user_type")
