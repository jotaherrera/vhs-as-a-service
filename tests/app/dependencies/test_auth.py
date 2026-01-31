import pytest
from pydantic import SecretStr
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.dependencies.auth import authenticate_user, get_current_active_user, get_current_user
from app.exceptions import NotFoundError, UnauthorizedError
from tests.factories.user import UserFactory


def test_authenticate_user(db_session: Session) -> None:
    password = "test-password"  # noqa: S105
    user = UserFactory.create(password=password)
    authenticated_user = authenticate_user(db_session, user.email, SecretStr(password))

    assert authenticated_user is not None


def test_authenticate_user_non_existent_user(db_session: Session) -> None:
    authenticated_user = authenticate_user(
        db_session,
        "wrong-email@mail.com",
        SecretStr("wrong-password"),
    )

    assert authenticated_user is None


def test_authenticate_user_wrong_password(db_session: Session) -> None:
    password = "test-password"  # noqa: S105
    user = UserFactory.create(password=password)

    authenticated_user = authenticate_user(db_session, user.email, SecretStr("wrong-password"))

    assert authenticated_user is None


def test_get_user(db_session: Session) -> None:
    user = UserFactory.create()
    token = create_access_token({"sub": str(user.id)})
    current_user = get_current_user(db_session, token)

    assert current_user == user


def test_get_user_not_user_id(db_session: Session) -> None:
    token = create_access_token({})

    with pytest.raises(UnauthorizedError, match="Credentials could not be validated"):
        get_current_user(db_session, token)


def test_get_user_not_found(db_session: Session) -> None:
    token = create_access_token({"sub": "123"})

    with pytest.raises(UnauthorizedError, match="Credentials could not be validated"):
        get_current_user(db_session, token)


def test_get_current_active_user() -> None:
    user = UserFactory.build(is_active=True)
    current_active_user = get_current_active_user(user)

    assert current_active_user == user


def test_get_current_active_user_not_active() -> None:
    user = UserFactory.build(is_active=False)

    with pytest.raises(NotFoundError, match="The user is not active"):
        get_current_active_user(user)
