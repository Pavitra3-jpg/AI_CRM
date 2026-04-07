from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from db import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(255), nullable=False)
    interaction_type = Column(String(100), nullable=False)
    product = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    sentiment = Column(String(100), nullable=True)
    concerns = Column(Text, nullable=True)
    follow_up = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)