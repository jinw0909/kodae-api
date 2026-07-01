from sqlalchemy import create_engine, func, cast
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings


# Create a database URL for SQLAlchemy
engine = create_engine(settings.MYSQL_VIEW, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:        
        db.close()