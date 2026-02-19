from sqlalchemy import Column, String, Text, Integer, DateTime, func
from database import Base

class URL(Base):
    __tablename__ = "urls"

    code = Column(String(20), primary_key=True, index=True)
    original_url = Column(Text, nullable=False)
    clicks = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

