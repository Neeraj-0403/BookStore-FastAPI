from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from repositories.base import Base


class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)