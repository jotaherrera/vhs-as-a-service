from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.movie.router import router as movies_router
from app.modules.rental.router import router as rentals_router
from app.modules.role.router import router as roles_router
from app.modules.user.router import router as users_router

router = APIRouter(prefix="/api/v1", tags=["v1"])

router.include_router(auth_router)
router.include_router(roles_router)
router.include_router(users_router)
router.include_router(movies_router)
router.include_router(rentals_router)
