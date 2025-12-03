from collections.abc import Generator

from sqlalchemy import Session, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import SETTINGS

ENGINE = create_engine(
    SETTINGS.database.connection_url,
    pool_pre_ping=True,
    echo=SETTINGS.debug,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

Base = declarative_base()

def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
