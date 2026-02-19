from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500))
    completed = Column(Boolean, default=False)
    priority = Column(Integer, default=1)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")

    
