from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
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
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    tickets = relationship("Ticket", back_populates="user")
