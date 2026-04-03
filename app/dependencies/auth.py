from typing import Annotated

from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import SecretStr

from app.core.security import decode_token, verify_password
from app.database.session import DbSession
from app.exceptions import NotFoundError, UnauthorizedError
from app.models import User
from app.operations.user import crud as crud_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


def authenticate_user(db: DbSession, email: str, password: SecretStr) -> User | None:
    db_user = crud_user.get_user_by_email(db, email)
    if db_user is None:
        return None

    if not verify_password(password.get_secret_value(), db_user.password):
        return None

    return db_user


def get_current_user(db: DbSession, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = UnauthorizedError(detail="Credentials could not be validated")

    payload = decode_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = crud_user.get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.is_active:
        raise NotFoundError(detail="The user is not active")

    return current_user
