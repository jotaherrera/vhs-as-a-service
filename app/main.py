from fastapi import FastAPI

from app.config import settings

app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    debug=settings.app.debug,
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
