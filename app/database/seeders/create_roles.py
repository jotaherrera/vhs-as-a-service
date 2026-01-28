import logging

from sqlalchemy.orm import Session

from app.operations.role import crud as crud_role
from app.operations.role.schemas import RoleCreate

LOGGER = logging.getLogger(__name__)


def create_roles(db: Session) -> None:
    roles = [
        RoleCreate(name="admin"),
        RoleCreate(name="user"),
    ]

    for role in roles:
        existing_role = crud_role.get_role_by_name(db, role.name)
        if existing_role:
            msg = f"Role {role.name} already exists"
            LOGGER.warning(msg)
            continue

        crud_role.create_role(db, role)
