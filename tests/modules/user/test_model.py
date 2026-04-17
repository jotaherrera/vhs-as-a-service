from tests.fakes.factories.user import UserFactory


def test_user_string_repr() -> None:
    user = UserFactory.build()

    expected = (
        f"<User(id={user.id}, "
        f"email={user.email!r}, "
        f"name={user.name!r}, "
        f"last_name={user.last_name!r}, "
        f"created_at={user.created_at}, "
        f"modified_at={user.modified_at}, "
        f"is_active={user.is_active}, "
        f"role={str(user.role.name)!r})>"
    )

    assert repr(user) == expected
