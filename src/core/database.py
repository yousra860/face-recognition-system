from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

# دعم SQLite و PostgreSQL
database_url = getattr(settings, 'get_database_url', settings.DATABASE_URL)

if database_url.startswith("sqlite"):
else:
    # PostgreSQL أو أي قاعدة أخرى
    engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
