from app.domains.auth.router import router as auth_router
from app.domains.users.router import router as user_router

__all__ = ["auth_router", "user_router"]
