from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
import datetime

class TicketsStatus(Base):
    __tablename__ = "tickets_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
