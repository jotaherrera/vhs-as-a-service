from typing import Annotated

from fastapi import Depends, FastAPI

from app.config import Settings, get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    debug=settings.app.debug,
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]) -> dict[str, str | bool]:
    return {
        "app_name": settings.app.name,
        "app_version": settings.app.version,
        "app_debug": settings.app.debug,
    }
