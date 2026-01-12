import logging
import os

from app.database.session import SessionLocal
from app.operations import role as crud_role
from app.operations import user as crud_user
from app.schemas.user import UserCreateInternal

LOGGER = logging.getLogger(__name__)


def safe_get_env(env_var: str) -> str:
    value = os.getenv(env_var)
    if not value:
        msg = f"Environment variable {env_var} is not set"
        raise ValueError(msg)

    return value


def create_super_user() -> None:
    password = safe_get_env("SUPER_USER_PASSWORD")
    email = safe_get_env("SUPER_USER_EMAIL")
    name = safe_get_env("SUPER_USER_NAME")
    last_name = safe_get_env("SUPER_USER_LAST_NAME")

    db = SessionLocal()
    try:
        admin_role = crud_role.get_role_by_name(db, "admin")
        if not admin_role or not admin_role.id:
            msg = "Admin role not found"
            raise ValueError(msg)

        admin_role_id = admin_role.id

        user = UserCreateInternal(
            email=email,
            password=password,
            name=name,
            last_name=last_name,
            role_id=admin_role_id,
            is_active=True,
        )

        existing_user = crud_user.get_user_by_email(db, email)
        if existing_user:
            msg = f"User {email} already exists"
            raise ValueError(msg)

        crud_user.create_user(db, user)

        msg = f"Super user {email} created successfully."
        LOGGER.info(msg)
    finally:
        db.close()
