from datetime import timedelta

from fastapi import APIRouter

from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token
from app.database.session import DbSession
from app.domains.auth.dependencies import authenticate_user
from app.domains.auth.schemas import TokenRequest, TokenResponse

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/token", tags=["token"])


@router.post("/")
async def get_access_token(db: DbSession, login_request: TokenRequest) -> TokenResponse:
    user = authenticate_user(db, login_request.email, login_request.password)
    if user is None:
        raise UnauthorizedError(detail="Invalid email or password")

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return TokenResponse(token=access_token, type="Bearer")
