from typing import Annotated

from fastapi import Depends, FastAPI

from app.config import Settings, get_settings
from app.handlers import add_exception_handlers
from app.routers import token_router, user_router

app = FastAPI(
    title=get_settings().app.name,
    version=get_settings().app.version,
    debug=get_settings().app.debug,
)

add_exception_handlers(app)

app.include_router(token_router)
app.include_router(user_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/info")
async def get_app_info(
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict[str, str | bool]:
    return {
        "app_name": settings.app.name,
        "app_version": settings.app.version,
        "app_debug": settings.app.debug,
    }
