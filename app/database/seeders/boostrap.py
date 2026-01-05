import logging

from app.database.seeders.create_roles import create_roles
from app.database.seeders.create_super_user import create_super_user

LOGGER = logging.getLogger(__name__)


def main() -> None:
    LOGGER.info("Seeding database...")

    create_roles()
    create_super_user()

    LOGGER.info("Database seeded successfully.")


if __name__ == "__main__":
    main()
