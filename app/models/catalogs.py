from sqlalchemy import Column, Integer, String
from app.core.database import Base


class TicketPriority(Base):
    __tablename__ = "tickets_priority"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class TicketType(Base):
    __tablename__ = "tickets_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class TicketCategory(Base):
    __tablename__ = "tickets_category"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
