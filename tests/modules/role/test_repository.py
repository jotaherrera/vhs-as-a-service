import pytest
from sqlalchemy.orm import Session

from app.modules.roles.model import Role, Roles
from app.modules.roles.repository import RoleRepository
from tests.factories.role import RoleFactory


@pytest.fixture
def role_repo(db_session: Session) -> RoleRepository:
    return RoleRepository(db_session)


def test_find_by_id_returns_role_when_exists(role_repo: RoleRepository) -> None:
    role = RoleFactory.create(name=Roles.STAFF)

    result = role_repo.find_by_id(role.id)

    assert result is not None
    assert result.id == role.id
    assert result.name == role.name


def test_find_by_id_returns_none_when_not_found(role_repo: RoleRepository) -> None:
    result = role_repo.find_by_id(999_999)

    assert result is None


def test_get_by_name_returns_role_when_exists(role_repo: RoleRepository) -> None:
    role = RoleFactory.create(name=Roles.CUSTOMER)

    result = role_repo.get_by_name(Roles.CUSTOMER)

    assert result is not None
    assert result.id == role.id
    assert result.name == role.name


def test_get_by_name_returns_none_when_not_found(role_repo: RoleRepository) -> None:
    result = role_repo.get_by_name("nonexistent-role")

    assert result is None


def test_get_all_returns_all_roles_without_filter(role_repo: RoleRepository) -> None:
    RoleFactory.create(name=Roles.STAFF)
    RoleFactory.create(name=Roles.CUSTOMER)

    result = role_repo.get_all()

    assert len(result) == 2


def test_get_all_with_is_active_true_returns_only_active(role_repo: RoleRepository) -> None:
    active = RoleFactory.create(name=Roles.STAFF, is_active=True)
    RoleFactory.create(name=Roles.CUSTOMER, is_active=False)

    result = role_repo.get_all(is_active=True)

    assert len(result) == 1
    assert result[0].id == active.id
    assert result[0].is_active is True


def test_get_all_with_is_active_false_returns_only_inactive(
    role_repo: RoleRepository,
) -> None:
    RoleFactory.create(name=Roles.STAFF, is_active=True)
    inactive = RoleFactory.create(name=Roles.CUSTOMER, is_active=False)

    result = role_repo.get_all(is_active=False)

    assert len(result) == 1
    assert result[0].id == inactive.id
    assert result[0].is_active is False


def test_create_persists_role_and_returns_it(
    role_repo: RoleRepository,
    db_session: Session,
) -> None:
    role = RoleFactory.build(name=Roles.STAFF)

    result = role_repo.create(role)

    assert result.id is not None
    assert db_session.get(Role, result.id) is not None
