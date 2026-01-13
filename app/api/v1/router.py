from fastapi import APIRouter

from app.api.v1.endpoints import token_router, user_router

router = APIRouter(prefix="/api/v1", tags=["v1"])

router.include_router(token_router)
router.include_router(user_router)
