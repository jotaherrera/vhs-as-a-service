from collections.abc import Generator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from app.database.session import get_db
from app.main import app

BASE_DIR = Path(__file__).resolve().parents[1]
ALEMBIC_INI_PATH = BASE_DIR / "alembic.ini"
MIGRATIONS_PATH = BASE_DIR / "app" / "database" / "alembic"

POSTGRES_IMAGE = "postgres:16-alpine"


def get_alembic_config(engine_url: str) -> Config:
    alembic_config = Config(str(ALEMBIC_INI_PATH))
    alembic_config.file_config.set("alembic", "script_location", str(MIGRATIONS_PATH))
    alembic_config.file_config.set("alembic", "sqlalchemy.url", engine_url)
    return alembic_config


def alembic_upgrade(url: str) -> None:
    try:
        alembic_config = get_alembic_config(url)
        command.upgrade(alembic_config, "head")
    except Exception as e:  # noqa: BLE001
        pytest.fail(f"Error upgrading database: {e}")


def alembic_downgrade(url: str) -> None:
    try:
        alembic_config = get_alembic_config(url)
        command.downgrade(alembic_config, "base")
    except Exception as e:  # noqa: BLE001
        pytest.fail(f"Error downgrading database: {e}")


@pytest.fixture(scope="session")
def engine() -> Generator[Engine]:
    with PostgresContainer(POSTGRES_IMAGE) as postgres:
        engine = create_engine(
            url=postgres.get_connection_url(),
            pool_pre_ping=True,
            echo=True,
            connect_args={
                "options": "-c search_path=app,public",
            },
        )
        try:
            yield engine
        finally:
            engine.dispose()


@pytest.fixture(scope="session")
def bootstrap_db(engine: Engine) -> Generator:
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS app"))

    yield

    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS app CASCADE"))


@pytest.fixture(scope="session")
def setup_database(engine: Engine, bootstrap_db: None) -> Generator:  # noqa: ARG001
    alembic_upgrade(engine.url.render_as_string(hide_password=False))

    yield

    alembic_downgrade(engine.url.render_as_string(hide_password=False))


@pytest.fixture
def test_session_local(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session(
    setup_database: None,  # noqa: ARG001
    engine: Engine,
    test_session_local: sessionmaker[Session],
) -> Generator[Session]:
    with engine.connect() as connection, connection.begin():
        session = test_session_local(bind=connection)
        try:
            yield session
        finally:
            session.close()


@pytest.fixture
def db_client(db_session: Session) -> Generator[TestClient]:
    def override_get_db() -> Generator[Session]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def simple_client() -> Generator[TestClient]:
    with TestClient(app) as c:
        yield c
