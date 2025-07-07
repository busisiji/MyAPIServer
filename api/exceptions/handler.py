# 异常统一处理
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from api.utils.exceptions import AppException

logger = logging.getLogger(__name__)

def add_exception_handlers(app):
    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception):
        if isinstance(exc, AppException):
            logger.warning(f"AppException: {exc.error_code}, Message: {exc.message}")
            return JSONResponse(
                status_code=exc.status_code,
                content={"error": exc.error_code, "message": exc.message}
            )
        else:
            logger.error("Unhandled exception occurred", exc_info=True, extra={
                "client_ip": request.client.host if request.client else "unknown",
                "url": str(request.url),
                "method": request.method,
                "error_type": type(exc).__name__,
                "message": str(exc)
            })
            return JSONResponse(
                status_code=500,
                content={"error": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred."}
            )

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        logger.warning(f"HTTP {exc.status_code} from {request.client.host}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": "HTTP_EXCEPTION", "message": exc.detail}
        )
