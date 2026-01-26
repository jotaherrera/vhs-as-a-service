from app.core.security import hash_password, verify_password


def test_password_hashing() -> None:
    password = "testpassword"  # noqa: S105
    hashed_password = hash_password(password)
    assert hashed_password is not None
    assert hashed_password != password


def test_password_verification() -> None:
    password = "testpassword"  # noqa: S105
    hashed_password = hash_password(password)
    assert verify_password(password, hashed_password)
