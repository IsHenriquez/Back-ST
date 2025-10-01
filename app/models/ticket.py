from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from app.core.database import Base
import datetime

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    address = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    fecha_ingreso_solicitud = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_realizar_servicio = Column(DateTime, nullable=True)
    fecha_termino_servicio = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
