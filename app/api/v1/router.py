from fastapi import APIRouter

from app.domains import auth_router, user_router

router = APIRouter(prefix="/api/v1", tags=["v1"])

router.include_router(auth_router)
router.include_router(user_router)
