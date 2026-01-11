from datetime import timedelta
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.security import create_access_token
from app.database.session import DbSession
from app.dependencies.auth import autenticate_user
from app.exceptions import UnautorizedError

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


class TokenRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    token: str
    type: Literal["Bearer"]


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
