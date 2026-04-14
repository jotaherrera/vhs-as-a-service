import pytest
from pydantic import SecretStr
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, UnauthorizedError
from app.core.security import create_access_token
from app.modules.auth.dependencies import (
    authenticate_user,
    get_current_active_user,
    get_current_user,
)
from app.modules.user.contracts import AbstractUserRepository
from app.modules.user.repository import UserRepository
from tests.fakes.factories.user import UserFactory


@pytest.fixture
def user_repo(db_session: Session) -> AbstractUserRepository:
    return UserRepository(db_session)


def test_authenticate_user(user_repo: AbstractUserRepository) -> None:
    password = "test-password"  # noqa: S105
    user = UserFactory.create(password=password)
    authenticated_user = authenticate_user(user_repo, user.email, SecretStr(password))

    assert authenticated_user is not None


def test_authenticate_user_non_existent_user(user_repo: AbstractUserRepository) -> None:
    authenticated_user = authenticate_user(
        user_repo,
        "wrong-email@mail.com",
        SecretStr("wrong-password"),
    )

    assert authenticated_user is None


def test_authenticate_user_wrong_password(user_repo: AbstractUserRepository) -> None:
    password = "test-password"  # noqa: S105
    user = UserFactory.create(password=password)

    authenticated_user = authenticate_user(user_repo, user.email, SecretStr("wrong-password"))

    assert authenticated_user is None


def test_get_user(user_repo: AbstractUserRepository) -> None:
    user = UserFactory.create()
    token = create_access_token({"sub": str(user.id)})
    current_user = get_current_user(user_repo, token)

    assert current_user == user


def test_get_user_not_user_id(user_repo: AbstractUserRepository) -> None:
    token = create_access_token({})

    with pytest.raises(UnauthorizedError, match="Credentials could not be validated"):
        get_current_user(user_repo, token)


def test_get_user_not_found(user_repo: AbstractUserRepository) -> None:
    token = create_access_token({"sub": "123"})

    with pytest.raises(UnauthorizedError, match="Credentials could not be validated"):
        get_current_user(user_repo, token)


def test_get_current_active_user() -> None:
    user = UserFactory.build(is_active=True)
    current_active_user = get_current_active_user(user)

    assert current_active_user == user


def test_get_current_active_user_not_active() -> None:
    user = UserFactory.build(is_active=False)

    with pytest.raises(NotFoundError, match="The user is not active"):
        get_current_active_user(user)
