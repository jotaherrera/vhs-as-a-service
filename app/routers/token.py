from datetime import timedelta
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

import app.operations.user as crud_user
from app.core.security import create_access_token, verify_password
from app.database.session import DbSession
from app.exceptions import UnautorizedError
from app.models.user import User

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


class TokenRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    token: str
    type: Literal["Bearer"]


def autenticate_user(db: DbSession, email: str, password: str) -> User | None:
    db_user = crud_user.get_user_by_email(db, email)
    if db_user is None:
        return None

    if not verify_password(password, db_user.password):
        return None

    return db_user


@router.post("/token")
async def get_access_token(db: DbSession, login_request: TokenRequest) -> TokenResponse:
    user = autenticate_user(db, login_request.email, login_request.password)
    if user is None:
        raise UnautorizedError(detail="Invalid email or password")

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return TokenResponse(token=access_token, type="Bearer")
