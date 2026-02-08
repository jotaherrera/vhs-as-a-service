import pytest
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.database.seeders.create_super_user import (
    DEFAULT_SUPER_USER_EMAIL,
    DEFAULT_SUPER_USER_LAST_NAME,
    DEFAULT_SUPER_USER_NAME,
    DEFAULT_SUPER_USER_PASSWORD,
    create_super_user,
)
from app.models import User
from tests.factories.role import RoleFactory
from tests.factories.user import UserFactory


def test_create_super_user(db_session: Session) -> None:
    role = RoleFactory.create(name="admin")
    role_id = role.id

    create_super_user(db_session)

    user = db_session.query(User).filter(User.email == DEFAULT_SUPER_USER_EMAIL).one()

    assert user.role_id == role_id
    assert user.name == DEFAULT_SUPER_USER_NAME
    assert user.last_name == DEFAULT_SUPER_USER_LAST_NAME
    assert user.is_active is True
    assert user.password != DEFAULT_SUPER_USER_PASSWORD
    assert verify_password(DEFAULT_SUPER_USER_PASSWORD, user.password)


def test_create_super_user_existing_user_error(db_session: Session) -> None:
    user = UserFactory.create(email=DEFAULT_SUPER_USER_EMAIL)

    with pytest.raises(ValueError, match=f"User {user.email} already exists"):
        create_super_user(db_session)


def test_create_super_user_admin_role_not_found(db_session: Session) -> None:
    with pytest.raises(ValueError, match="Admin role not found"):
        create_super_user(db_session)
