from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from core.config import settings

class Base(DeclarativeBase):
    pass

engine=create_engine(settings.DATABASE_URL, fast_executemany=False,echo=False,future=True)
SessionLocal=sessionmaker(bind=engine,autoflush=True,autocommit=False)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()