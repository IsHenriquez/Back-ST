from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
import datetime

class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    last_name = Column(String(50), nullable=True)
    mother_last_name = Column(String(50), nullable=True)
    identification_number = Column(String(20), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
