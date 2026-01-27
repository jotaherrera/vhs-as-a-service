from datetime import datetime, timedelta

import jwt
import pytest
from dateutil.tz import UTC
from freezegun import freeze_time

from app.config import get_settings
from app.core.security import (
    ALGORITHM,
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.exceptions import UnauthorizedError

TOKEN_TO_EXPIRE_MINUTES = 5


@freeze_time("2025-01-01 12:00:00")
def test_create_access_token() -> None:
    user_id = "123"
    expires_delta = timedelta(minutes=TOKEN_TO_EXPIRE_MINUTES)

    token = create_access_token(
        {"sub": user_id},
        expires_delta=expires_delta,
    )

    decoded_token = jwt.decode(
        token.strip(),
        key=get_settings().app.jwt_secret,
        algorithms=ALGORITHM,
    )

    expires = datetime.now(tz=UTC) + expires_delta

    assert decoded_token["sub"] == user_id
    assert decoded_token["exp"] == int(expires.timestamp())


@freeze_time("2025-01-01 12:00:00")
def test_decode_token() -> None:
    user_id = "123"
    expires_delta = timedelta(minutes=TOKEN_TO_EXPIRE_MINUTES)
    expires = datetime.now(UTC) + expires_delta

    to_encode = {
        "sub": user_id,
        "exp": expires,
    }
    token = jwt.encode(payload=to_encode, key=get_settings().app.jwt_secret, algorithm=ALGORITHM)

    decoded_token = decode_token(token)

    assert decoded_token["sub"] == user_id
    assert decoded_token["exp"] == int(expires.timestamp())


def test_decode_token_malformed_token() -> None:
    token = "token-123-45"  # noqa: S105

    with pytest.raises(UnauthorizedError, match="Could not validate credentials"):
        decode_token(token)


@freeze_time("2025-01-01 12:00:00")
def test_decode_token_expired_token() -> None:
    token = create_access_token({"sub": "123"}, expires_delta=timedelta(minutes=-1))

    with pytest.raises(UnauthorizedError, match="Could not validate credentials"):
        decode_token(token)


def test_decode_token_with_wrong_signature() -> None:
    token = jwt.encode({"sub": "123"}, "wrong-secret", algorithm=ALGORITHM)

    with pytest.raises(UnauthorizedError):
        decode_token(token)


def test_password_hashing() -> None:
    password = "testpassword"  # noqa: S105
    hashed_password = hash_password(password)
    assert hashed_password is not None
    assert hashed_password != password


def test_password_verification() -> None:
    password = "testpassword"  # noqa: S105
    hashed_password = hash_password(password)
    assert verify_password(password, hashed_password)


def test_password_verification_error() -> None:
    password = "testpassword"  # noqa: S105
    hashed_password = hash_password(password)
    assert not verify_password("wrong-password", hashed_password)
