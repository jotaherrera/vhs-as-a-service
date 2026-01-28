from sqlalchemy.orm import Session

from app.operations.role.crud import create_role, get_all_roles, get_role_by_id, get_role_by_name
from app.operations.role.schemas import RoleCreate
from tests.factories.role import RoleFactory


def test_get_all_roles(db_session: Session) -> None:
    role_1 = RoleFactory.create(name="admin")
    role_2 = RoleFactory.create(name="user")

    all_roles = get_all_roles(db_session)

    returned_ids = {r.id for r in all_roles}

    assert returned_ids == {role_1.id, role_2.id}


def test_get_role_by_name(db_session: Session) -> None:
    role = RoleFactory.create(name="user")

    db_role = get_role_by_name(db_session, "user")

    assert db_role is not None
    assert db_role.id == role.id
    assert db_role.name == role.name


def test_get_role_by_id(db_session: Session) -> None:
    role = RoleFactory.create(name="admin")

    db_role = get_role_by_id(db_session, role.id)

    assert db_role is not None
    assert db_role.id == role.id
    assert db_role.name == role.name


def test_create_role(db_session: Session) -> None:
    role_create = RoleCreate(name="user", is_active=True)

    created_role = create_role(db_session, role_create)

    assert created_role.name == role_create.name
    assert created_role.is_active == role_create.is_active
