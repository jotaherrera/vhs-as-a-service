import pytest
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.database.seeders.create_super_user import create_super_user, safe_get_env
from app.models import User
from tests.factories.role import RoleFactory
from tests.factories.user import UserFactory


def test_get_set_env(monkeypatch: pytest.MonkeyPatch) -> None:
    env_var = "test-env-var"
    monkeypatch.setenv("ENV_VAR_1", env_var)

    result_env_var = safe_get_env("ENV_VAR_1")

    assert result_env_var == env_var


def test_get_set_env_not_set() -> None:
    env_var_name = "ENV_VAR_1"

    with pytest.raises(ValueError, match=f"Environment variable {env_var_name} is not set"):
        safe_get_env(env_var_name)


def test_create_super_user(db_session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    role = RoleFactory.create(name="admin")
    role_id = role.id

    password = "test-password"  # noqa: S105

    monkeypatch.setenv("SUPER_USER_PASSWORD", password)
    monkeypatch.setenv("SUPER_USER_EMAIL", "super@email.com")
    monkeypatch.setenv("SUPER_USER_NAME", "Super")
    monkeypatch.setenv("SUPER_USER_LAST_NAME", "User")

    create_super_user(db_session)

    user = db_session.query(User).filter(User.email == "super@email.com").one()

    assert user.role_id == role_id
    assert user.name == "Super"
    assert user.last_name == "User"
    assert user.is_active is True
    assert user.password != password
    assert verify_password(password, user.password)


def test_create_super_user_existing_user_error(
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user = UserFactory.create(email="super@email.com")

    monkeypatch.setenv("SUPER_USER_PASSWORD", "test-password")
    monkeypatch.setenv("SUPER_USER_EMAIL", "super@email.com")
    monkeypatch.setenv("SUPER_USER_NAME", "Super")
    monkeypatch.setenv("SUPER_USER_LAST_NAME", "User")

    with pytest.raises(ValueError, match=f"User {user.email} already exists"):
        create_super_user(db_session)


def test_create_super_user_admin_role_not_found(
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SUPER_USER_PASSWORD", "test-password")
    monkeypatch.setenv("SUPER_USER_EMAIL", "super@email.com")
    monkeypatch.setenv("SUPER_USER_NAME", "Super")
    monkeypatch.setenv("SUPER_USER_LAST_NAME", "User")

    with pytest.raises(ValueError, match="Admin role not found"):
        create_super_user(db_session)
