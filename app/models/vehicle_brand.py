from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
import datetime

class VehicleBrand(Base):
    __tablename__ = "vehicles_brand"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
