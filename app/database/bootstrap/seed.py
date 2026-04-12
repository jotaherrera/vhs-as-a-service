import logging

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.database.infrastructure.session import SessionLocal
from app.modules.role.model import Role, RoleName
from app.modules.user.model import User

LOGGER = logging.getLogger(__name__)

STAFF_USER = {
    "email": "staff@vhsaas.com",
    "password": "staff1234",
    "name": "Staff",
    "last_name": "User",
}


def seed_roles(db: Session) -> None:
    for name in RoleName:
        exists = db.query(Role).filter(Role.name == name).first()

        if not exists:
            db.add(Role(name=name, is_active=True))

    db.commit()
    LOGGER.info("Roles seeded.")


def seed_staff(db: Session) -> None:
    if db.query(User).filter(User.email == STAFF_USER["email"]).first():
        LOGGER.info("Staff user already exists, skipping.")
        return

    staff_role = db.query(Role).filter(Role.name == RoleName.STAFF).one()

    db.add(
        User(
            email=STAFF_USER["email"],
            password=hash_password(STAFF_USER["password"]),
            name=STAFF_USER["name"],
            last_name=STAFF_USER["last_name"],
            role_id=staff_role.id,
            is_active=True,
        ),
    )

    db.commit()
    LOGGER.info("Staff user seeded.")


def main() -> None:
    db = SessionLocal()
    try:
        seed_roles(db)
        seed_staff(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
