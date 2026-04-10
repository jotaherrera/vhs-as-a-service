from fastapi import APIRouter

from app.database.infrastructure.session import DbSession
from app.modules.auth import service as auth_service
from app.modules.auth.schemas import TokenCreate, TokenResponse

router = APIRouter(prefix="/token", tags=["token"])


@router.post("/")
async def get_access_token(db: DbSession, token_request: TokenCreate) -> TokenResponse:
    access_token = auth_service.generate_token(db, token_request)
    return TokenResponse(token=access_token, type="Bearer")
