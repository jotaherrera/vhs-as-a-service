from datetime import timedelta

from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token
from app.modules.auth.dependencies import authenticate_user
from app.modules.auth.schemas import TokenCreate
from app.modules.users.contracts import AbstractUserRepository

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def generate_token(user_repo: AbstractUserRepository, token_request: TokenCreate) -> str:
    user = authenticate_user(user_repo, token_request.email, token_request.password)
    if user is None:
        raise UnauthorizedError(detail="Invalid email or password")

    return create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
