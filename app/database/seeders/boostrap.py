import logging

from app.database.seeders.create_roles import create_roles
from app.database.seeders.create_super_user import create_super_user
from app.database.session import SessionLocal

LOGGER = logging.getLogger(__name__)


def main() -> None:
    LOGGER.info("Seeding database...")

    db = SessionLocal()
    try:
        create_roles(db)
        create_super_user(db)
        LOGGER.info("Database seeded successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
