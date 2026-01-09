import logging

from app.database.session import SessionLocal
from app.operations import role as crud_role
from app.schemas.role import RoleCreate

LOGGER = logging.getLogger(__name__)


def create_roles() -> None:
    roles = [
        RoleCreate(name="admin"),
        RoleCreate(name="user"),
    ]

    db = SessionLocal()
    try:
        for role in roles:
            existing_role = crud_role.get_role_by_name(db, role.name)
            if existing_role:
                msg = f"Role {role.name} already exists"
                LOGGER.warning(msg)
                continue

            crud_role.create_role(db, role)
    finally:
        db.close()
