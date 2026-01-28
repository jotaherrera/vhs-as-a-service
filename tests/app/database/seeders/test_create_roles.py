import logging

import pytest
from sqlalchemy.orm import Session

from app.database.seeders.create_roles import create_roles
from app.models import Role
from tests.factories.role import RoleFactory


def test_create_roles(db_session: Session) -> None:
    create_roles(db_session)

    all_roles = db_session.query(Role).all()

    returned_names = {r.name for r in all_roles}

    assert returned_names == {"admin", "user"}


def test_create_roles_name_already_exists(
    db_session: Session,
    caplog: pytest.LogCaptureFixture,
) -> None:
    role = RoleFactory.create(name="user")

    with caplog.at_level(logging.WARNING):
        create_roles(db_session)

    assert f"Role {role.name} already exists" in caplog.text
