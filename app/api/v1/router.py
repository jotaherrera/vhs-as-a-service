from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as user_router

router = APIRouter(prefix="/api/v1", tags=["v1"])

router.include_router(auth_router)
router.include_router(user_router)
