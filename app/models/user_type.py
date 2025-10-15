# app/models/user_type.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserType(Base):
    __tablename__ = "users_type"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    
    # Relación inversa
    users = relationship("User", back_populates="user_type")
