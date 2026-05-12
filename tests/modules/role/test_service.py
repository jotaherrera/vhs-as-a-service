import pytest

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.modules.role.model import RoleName
from app.modules.role.schemas import RoleCreate, RoleResponse
from app.modules.role.service import RoleService
from tests.fakes.factories.role import RoleFactory
from tests.fakes.factories.user import UserFactory
from tests.fakes.repository import FakeRoleRepository


def test_list_roles_raises_forbidden_for_non_staff() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    service = RoleService(role_repo=FakeRoleRepository())

    with pytest.raises(ForbiddenError):
        service.list_roles(user)


def test_list_roles_returns_all_roles_for_staff() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    service = RoleService(
        role_repo=FakeRoleRepository(
            roles=[
                RoleFactory.build(name=RoleName.STAFF),
                RoleFactory.build(name=RoleName.CUSTOMER),
            ],
        ),
    )

    result = service.list_roles(user)

    assert result.total == 2
    assert len(result.roles) == 2


def test_list_roles_returns_role_response_schema() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    role = RoleFactory.build(name=RoleName.CUSTOMER)
    service = RoleService(role_repo=FakeRoleRepository(roles=[role]))

    result = service.list_roles(user)

    assert len(result.roles) == 1
    item = result.roles[0]
    assert isinstance(item, RoleResponse)
    assert item.id == role.id
    assert item.name == role.name


def test_get_by_id_raises_forbidden_for_non_staff() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    service = RoleService(role_repo=FakeRoleRepository())

    with pytest.raises(ForbiddenError):
        service.get_by_id(user, role_id=1)


def test_get_by_id_raises_not_found_for_missing_role() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    service = RoleService(role_repo=FakeRoleRepository())

    with pytest.raises(NotFoundError):
        service.get_by_id(user, role_id=999)


def test_get_by_id_returns_correct_role() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    role = RoleFactory.build(name=RoleName.CUSTOMER)
    service = RoleService(role_repo=FakeRoleRepository(roles=[role]))

    result = service.get_by_id(user, role_id=role.id)

    assert isinstance(result, RoleResponse)
    assert result.id == role.id
    assert result.name == role.name


def test_non_staff_cannot_register_role() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    service = RoleService(role_repo=FakeRoleRepository())
    request = RoleCreate(name=RoleName.STAFF, is_active=True)

    with pytest.raises(ForbiddenError):
        service.register(user, request)


def test_register_raises_conflict_when_name_already_exists() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    existing = RoleFactory.build(name=RoleName.CUSTOMER)
    service = RoleService(role_repo=FakeRoleRepository(roles=[existing]))
    request = RoleCreate(name=RoleName.CUSTOMER, is_active=True)

    with pytest.raises(ConflictError) as exc_info:
        service.register(user, request)

    assert RoleName.CUSTOMER.value.lower() in exc_info.value.detail.lower()


def test_register_persists_and_returns_role_response() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    service = RoleService(role_repo=FakeRoleRepository())
    request = RoleCreate(name=RoleName.STAFF, is_active=True)

    result = service.register(user, request)

    assert isinstance(result, RoleResponse)
    assert result.name == RoleName.STAFF


def test_remove_raises_forbidden_for_non_staff() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    service = RoleService(role_repo=FakeRoleRepository())

    with pytest.raises(ForbiddenError):
        service.remove(user, role_id=1)


def test_remove_raises_not_found_for_missing_role() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    service = RoleService(role_repo=FakeRoleRepository())

    with pytest.raises(NotFoundError):
        service.remove(user, role_id=999)


def test_remove_successful() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    role = RoleFactory.build()
    service = RoleService(role_repo=FakeRoleRepository(roles=[role]))

    service.remove(user, role_id=role.id)
