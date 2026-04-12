from typing import Annotated

from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import SecretStr

from app.core.exceptions import NotFoundError, UnauthorizedError
from app.core.security import decode_token, verify_password
from app.modules.user.model import User
from app.modules.user.repository import UserRepo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


def authenticate_user(user_repo: UserRepo, email: str, password: SecretStr) -> User | None:
    db_user = user_repo.get_by_email(email)
    if db_user is None:
        return None

    if not verify_password(password.get_secret_value(), db_user.password):
        return None

    return db_user


def get_current_user(user_repo: UserRepo, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = UnauthorizedError(detail="Credentials could not be validated")

    payload = decode_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = user_repo.find_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.is_active:
        raise NotFoundError(detail="The user is not active")

    return current_user
