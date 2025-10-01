from sqlalchemy import Column, Integer, String, SmallInteger, Boolean, DateTime, ForeignKey
from app.core.database import Base
import datetime

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    id_vehicle_model = Column(Integer, ForeignKey("vehicles_model.id"), nullable=False)
    is_busy = Column(Boolean, default=False)
    active = Column(SmallInteger, default=1)
    plate = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
