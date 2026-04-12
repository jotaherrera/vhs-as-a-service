import pytest
from sqlalchemy.orm import Session

from app.modules.users.model import User
from app.modules.users.repository import UserRepository
from tests.factories.user import UserFactory


@pytest.fixture
def user_repo(db_session: Session) -> UserRepository:
    return UserRepository(db_session)


def test_find_by_id_returns_user_when_exists(user_repo: UserRepository) -> None:
    user = UserFactory.create()

    result = user_repo.find_by_id(user.id)

    assert result is not None
    assert result.id == user.id
    assert result.email == user.email


def test_find_by_id_returns_none_when_not_found(user_repo: UserRepository) -> None:
    result = user_repo.find_by_id(999_999)

    assert result is None


def test_get_by_email_returns_user_when_exists(user_repo: UserRepository) -> None:
    user = UserFactory.create()

    result = user_repo.get_by_email(user.email)

    assert result is not None
    assert result.id == user.id
    assert result.email == user.email


def test_get_by_email_returns_none_when_not_found(user_repo: UserRepository) -> None:
    result = user_repo.get_by_email("nonexistent@mail.com")

    assert result is None


def test_get_all_returns_all_users_without_filter(user_repo: UserRepository) -> None:
    UserFactory.create(is_active=True)
    UserFactory.create(is_active=False)

    result = user_repo.get_all()

    assert len(result) == 2


def test_get_all_with_is_active_true_returns_only_active(user_repo: UserRepository) -> None:
    active = UserFactory.create(is_active=True)
    UserFactory.create(is_active=False)

    result = user_repo.get_all(is_active=True)

    assert len(result) == 1
    assert result[0].id == active.id
    assert result[0].is_active is True


def test_get_all_with_is_active_false_returns_only_inactive(
    user_repo: UserRepository,
) -> None:
    UserFactory.create(is_active=True)
    inactive = UserFactory.create(is_active=False)

    result = user_repo.get_all(is_active=False)

    assert len(result) == 1
    assert result[0].id == inactive.id
    assert result[0].is_active is False


def test_create_persists_user_and_returns_it(
    user_repo: UserRepository,
    db_session: Session,
) -> None:
    user = UserFactory.build()

    result = user_repo.create(user)

    assert result.id is not None
    assert db_session.get(User, result.id) is not None
