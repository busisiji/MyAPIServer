# app/exceptions/handler.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from app.utils.exceptions import AppException

logger = logging.getLogger(__name__)

def add_exception_handlers(app):
    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception):
        if isinstance(exc, AppException):
            extra = {
                "client_ip": request.client.host if request.client else "unknown",
                "method": request.method,
                "path": request.url.path,
                "error_type": type(exc).__name__,
                "error_code": exc.error_code,
                "message": exc.message
            }
            logger.warning("App exception occurred", extra=extra)
            return JSONResponse(
                status_code=exc.status_code,
                content={"error": exc.error_code, "message": exc.message}
            )
        else:
            extra = {
                "client_ip": request.client.host if request.client else "unknown",
                "method": request.method,
                "path": request.url.path,
                "error_type": type(exc).__name__,
                "message": str(exc)
            }
            logger.error("Unhandled exception occurred", exc_info=True, extra=extra)
            return JSONResponse(
                status_code=500,
                content={"error": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred."}
            )

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        extra = {
            "client_ip": request.client.host if request.client else "unknown",
            "method": request.method,
            "path": request.url.path,
            "status_code": exc.status_code,
            "message": exc.detail
        }
        logger.warning("HTTP exception", extra=extra)
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": "HTTP_EXCEPTION", "message": exc.detail}
        )
