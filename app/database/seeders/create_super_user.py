import logging

from pydantic import SecretStr
from sqlalchemy.orm import Session

from app.operations.role import crud as crud_role
from app.operations.user import crud as crud_user
from app.operations.user.schemas import UserCreate

LOGGER = logging.getLogger(__name__)

# Hardcoded values for easier demonstration purposes
# This should be avoided in production
SUPER_USER_EMAIL = "admin@email.com"
SUPER_USER_PASSWORD = "012345678"  # noqa: S105
SUPER_USER_NAME = "Admin"
SUPER_USER_LAST_NAME = "User"


def create_super_user(db: Session) -> None:
    existing_user = crud_user.get_user_by_email(db, SUPER_USER_EMAIL)
    if existing_user:
        msg = f"User {SUPER_USER_EMAIL} already exists"
        raise ValueError(msg)

    admin_role = crud_role.get_role_by_name(db, "admin")
    if not admin_role:
        msg = "Admin role not found"
        raise ValueError(msg)

    user = UserCreate(
        email=SUPER_USER_EMAIL,
        password=SecretStr(SUPER_USER_PASSWORD),
        name=SUPER_USER_NAME,
        last_name=SUPER_USER_LAST_NAME,
        role_id=admin_role.id,
        is_active=True,
    )

    crud_user.create_user(db, user)

    msg = f"Super user {SUPER_USER_EMAIL} created successfully."
    LOGGER.info(msg)
