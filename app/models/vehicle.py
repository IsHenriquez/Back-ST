# app/models/vehicle.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.core.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    id_vehicle_model = Column(Integer, ForeignKey("vehicles_model.id"), nullable=True)  # ✅ nullable=True
    plate = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    is_busy = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
