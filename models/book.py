from sqlalchemy import Column,Integer,String,DateTime
from repositories.base import Base
from datetime import datetime

class Book(Base):
    __tablename__ = "books"
 
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String,nullable=False)
    author = Column(String,  nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)