from tests.factories.user import UserFactory


def test_user_string_repr() -> None:
    user = UserFactory.build()

    expected = (
        f"User(id={user.id}, email={user.email}, name={user.name}, last_name={user.last_name}, "
        f"created_at={user.created_at}, modified_at={user.modified_at}, "
        f"is_active={user.is_active}, role={user.role.name})"
    )

    assert repr(user) == expected
