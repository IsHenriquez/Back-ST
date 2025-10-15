from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    id_managing_user = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    user_id          = Column(BigInteger, ForeignKey("users.id"), nullable=True)  # técnico asignado

    id_status   = Column(BigInteger, ForeignKey("tickets_status.id"), nullable=False)
    id_type     = Column(BigInteger, ForeignKey("tickets_type.id"),   nullable=False)
    id_category = Column(BigInteger, ForeignKey("tickets_category.id"), nullable=False)
    id_priority = Column(BigInteger, ForeignKey("tickets_priority.id"), nullable=False)
    id_customer = Column(BigInteger, ForeignKey("customer.id"), nullable=True)

    title   = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    address = Column(String(255), nullable=True)
    latitude  = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    fecha_ingreso_solicitud  = Column(DateTime, nullable=True, index=True)
    fecha_realizar_servicio  = Column(DateTime, nullable=True, index=True)  # <- para “hoy”
    fecha_termino_servicio   = Column(DateTime, nullable=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    managing_user = relationship("User", foreign_keys=[id_managing_user], back_populates="tickets_managing")
    user          = relationship("User", foreign_keys=[user_id],          back_populates="tickets_in_charge")
