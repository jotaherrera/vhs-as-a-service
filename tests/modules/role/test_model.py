import pytest

from tests.factories.role import RoleFactory


def test_role_string_repr() -> None:
    role = RoleFactory.build()

    expected = (
        f"Role(id={role.id}, name={str(role.name)!r}, is_active={role.is_active}, "
        f"created_at={role.created_at}, modified_at={role.modified_at})"
    )

    assert repr(role) == expected


def test_create_role_with_invalid_name() -> None:
    with pytest.raises(ValueError, match="Invalid role:"):
        RoleFactory.build(name="INVALID")
