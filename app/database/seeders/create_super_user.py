import logging
import os
from typing import NamedTuple

from pydantic import SecretStr
from sqlalchemy.orm import Session

from app.operations.role import crud as crud_role
from app.operations.user import crud as crud_user
from app.operations.user.schemas import UserCreate

LOGGER = logging.getLogger(__name__)

# Hardcoded values for easier demonstration purposes
# This should be avoided in production
DEFAULT_SUPER_USER_EMAIL = "admin@email.com"
DEFAULT_SUPER_USER_PASSWORD = "012345678"  # noqa: S105
DEFAULT_SUPER_USER_NAME = "Admin"
DEFAULT_SUPER_USER_LAST_NAME = "User"


class SuperUserInfo(NamedTuple):
    email: str
    password: str
    name: str
    last_name: str


def get_super_user_info() -> SuperUserInfo:
    email = os.getenv("SUPER_USER_EMAIL", DEFAULT_SUPER_USER_EMAIL)
    password = os.getenv("SUPER_USER_PASSWORD", DEFAULT_SUPER_USER_PASSWORD)
    name = os.getenv("SUPER_USER_NAME", DEFAULT_SUPER_USER_NAME)
    last_name = os.getenv("SUPER_USER_LAST_NAME", DEFAULT_SUPER_USER_LAST_NAME)
    return SuperUserInfo(email, password, name, last_name)


def create_super_user(db: Session) -> None:
    super_user_info = get_super_user_info()

    existing_user = crud_user.get_user_by_email(db, super_user_info.email)
    if existing_user:
        msg = f"User {super_user_info.email} already exists"
        raise ValueError(msg)

    admin_role = crud_role.get_role_by_name(db, "admin")
    if not admin_role:
        msg = "Admin role not found"
        raise ValueError(msg)

    user = UserCreate(
        email=super_user_info.email,
        password=SecretStr(super_user_info.password),
        name=super_user_info.name,
        last_name=super_user_info.last_name,
        role_id=admin_role.id,
        is_active=True,
    )

    crud_user.create_user(db, user)

    msg = f"Super user {super_user_info.email} created successfully."
    LOGGER.info(msg)
