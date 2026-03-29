import logging

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.database.session import SessionLocal
from app.models import Role, User

LOGGER = logging.getLogger(__name__)

SEED_ROLES = ["admin", "user"]

ADMIN_USER = {
    "email": "admin@vhsaas.com",
    "password": "admin1234",
    "name": "Admin",
    "last_name": "User",
}


def seed_roles(db: Session) -> None:
    for name in SEED_ROLES:
        if not db.query(Role).filter(Role.name == name).first():
            db.add(Role(name=name, is_active=True))

    db.commit()
    LOGGER.info("Roles seeded.")


def seed_admin(db: Session) -> None:
    if db.query(User).filter(User.email == ADMIN_USER["email"]).first():
        LOGGER.info("Admin user already exists, skipping.")
        return

    admin_role = db.query(Role).filter(Role.name == "admin").one()

    db.add(
        User(
            email=ADMIN_USER["email"],
            password=hash_password(ADMIN_USER["password"]),
            name=ADMIN_USER["name"],
            last_name=ADMIN_USER["last_name"],
            role_id=admin_role.id,
            is_active=True,
        ),
    )

    db.commit()
    LOGGER.info("Admin user seeded.")


def main() -> None:
    db = SessionLocal()
    try:
        seed_roles(db)
        seed_admin(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
