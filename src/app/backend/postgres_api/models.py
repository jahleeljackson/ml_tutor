from sqlalchemy import Column, Integer, Text, DateTime, String
from sqlalchemy.sql import func
from .database import Base 


class Conversation(Base):
    __tablename__ = "conversations"

    context_id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    model = Column(String)
    context_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
