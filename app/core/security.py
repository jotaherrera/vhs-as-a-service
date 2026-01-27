from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

from app.config import get_settings
from app.exceptions import UnauthorizedError

ALGORITHM = "HS256"
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    to_encode = data.copy()
    expires = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expires})

    return jwt.encode(payload=to_encode, key=get_settings().app.jwt_secret, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token.strip(), key=get_settings().app.jwt_secret, algorithms=ALGORITHM)
    except jwt.InvalidTokenError as err:
        raise UnauthorizedError(detail="Could not validate credentials") from err


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
