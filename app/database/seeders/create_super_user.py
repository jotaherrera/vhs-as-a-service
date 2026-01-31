import logging
import os

from pydantic import SecretStr
from sqlalchemy.orm import Session

from app.operations.role import crud as crud_role
from app.operations.user import crud as crud_user
from app.operations.user.schemas import UserCreate

LOGGER = logging.getLogger(__name__)


def safe_get_env(env_var: str) -> str:
    value = os.getenv(env_var)
    if not value:
        msg = f"Environment variable {env_var} is not set"
        raise ValueError(msg)

    return value


def create_super_user(db: Session) -> None:
    password = safe_get_env("SUPER_USER_PASSWORD")
    email = safe_get_env("SUPER_USER_EMAIL")
    name = safe_get_env("SUPER_USER_NAME")
    last_name = safe_get_env("SUPER_USER_LAST_NAME")

    existing_user = crud_user.get_user_by_email(db, email)
    if existing_user:
        msg = f"User {email} already exists"
        raise ValueError(msg)

    admin_role = crud_role.get_role_by_name(db, "admin")
    if not admin_role:
        msg = "Admin role not found"
        raise ValueError(msg)

    user = UserCreate(
        email=email,
        password=SecretStr(password),
        name=name,
        last_name=last_name,
        role_id=admin_role.id,
        is_active=True,
    )

    crud_user.create_user(db, user)

    msg = f"Super user {email} created successfully."
    LOGGER.info(msg)
