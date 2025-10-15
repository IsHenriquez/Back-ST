from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    active = Column(Boolean, default=True)
    id_user_type = Column(Integer, nullable=True)
    id_vehicle = Column(Integer, nullable=True)
    name = Column(String(255), nullable=False)
    last_name = Column(String(50), nullable=True)
    mother_last_name = Column(String(50), nullable=True)
    identification_number = Column(String(20), nullable=True)
    gender = Column(String(1), nullable=True)
    birth_date = Column(Date, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    email_verified_at = Column(DateTime, nullable=True)
    password = Column(String(255), nullable=True)
    remember_token = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    id_user_type = Column(Integer, ForeignKey("users_type.id"), nullable=True)  # ✅ BUENO

    tickets_managing = relationship(
        "Ticket",
        foreign_keys="[Ticket.id_managing_user]",
        back_populates="managing_user"
    )
    
    tickets_in_charge = relationship(
        "Ticket",
        foreign_keys="[Ticket.user_id]",
        back_populates="user"
    )
