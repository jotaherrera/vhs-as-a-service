import pytest

from app.core.exceptions import ConflictError
from app.modules.role.model import Role, RoleName
from app.modules.role.service import RoleService
from tests.fakes.repository import FakeRoleRepository


def test_create_role_persists_correctly() -> None:
    service = RoleService(role_repo=FakeRoleRepository())

    role = Role(name=RoleName.CUSTOMER)

    result = service.create_role(role)

    assert result is role
    assert len(service.role_repo.get_all()) == 1
    assert service.role_repo.get_all()[0].name == RoleName.CUSTOMER


def test_create_role_raises_conflict_for_existing_role() -> None:
    existing_role = Role(name=RoleName.STAFF)
    service = RoleService(role_repo=FakeRoleRepository(roles=[existing_role]))

    role = Role(name=RoleName.STAFF)

    with pytest.raises(ConflictError) as exc_info:
        service.create_role(role)

    assert "STAFF already exists" in exc_info.value.detail
