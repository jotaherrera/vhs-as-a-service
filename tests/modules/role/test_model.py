from tests.factories.role import RoleFactory


def test_role_string_repr() -> None:
    role = RoleFactory.build()

    expected = (
        f"<Role(id={role.id}, "
        f"name={str(role.name)!r}, "
        f"is_active={role.is_active}, "
        f"created_at={role.created_at}, "
        f"modified_at={role.modified_at})>"
    )

    assert repr(role) == expected
