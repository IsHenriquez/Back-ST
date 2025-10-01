from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base
import datetime

class VehicleModel(Base):
    __tablename__ = "vehicles_model"

    id = Column(Integer, primary_key=True, index=True)
    id_vehicles_brand = Column(Integer, ForeignKey("vehicles_brand.id"), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
