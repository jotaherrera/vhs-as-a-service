from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import SETTINGS

ENGINE = create_engine(
    SETTINGS.database.connection_url,
    pool_pre_ping=True,
    echo=SETTINGS.app_debug,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
