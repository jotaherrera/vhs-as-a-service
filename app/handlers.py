import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        logger.error(
            "HTTP Error on %s: %s",
            request.url,
            exc.detail,
            exc_info=(type(exc), exc, exc.__traceback__),
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "route": str(request.url)},
            headers=exc.headers,
        )
