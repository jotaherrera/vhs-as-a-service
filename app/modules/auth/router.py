from fastapi import APIRouter

from app.modules.auth import service as auth_service
from app.modules.auth.schemas import TokenCreate, TokenResponse
from app.modules.user.repository import UserRepo

router = APIRouter(prefix="/token", tags=["token"])


@router.post("/")
async def get_access_token(user_repo: UserRepo, token_request: TokenCreate) -> TokenResponse:
    access_token = auth_service.generate_token(user_repo, token_request)
    return TokenResponse(token=access_token, type="Bearer")
