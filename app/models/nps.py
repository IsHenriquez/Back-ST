from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class NPS(Base):
    __tablename__ = "nps"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, nullable=False)
    id_customer = Column(Integer, nullable=False)
    id_ticket = Column(Integer, nullable=False)
    evaluation = Column(Integer, nullable=False)
