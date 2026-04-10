from typing import Annotated

from fastapi import Depends, FastAPI

from app.api.v1 import v1_router
from app.core.config import Settings, get_settings
from app.core.handlers import add_exception_handlers

app = FastAPI(
    title=get_settings().app.name,
    version=get_settings().app.version,
    debug=get_settings().app.debug,
)

add_exception_handlers(app)

app.include_router(v1_router)


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
