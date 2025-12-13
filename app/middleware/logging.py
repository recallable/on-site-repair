import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from fastapi import Request, FastAPI

from app.middleware.exception import ExceptionHandlerMiddleware

logger = logging.getLogger("app")


class AccessLogHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        start_time = time.time()
        response = await call_next(request)
        cost = time.time() - start_time
        logger.info(
            "%s %s %s %.3fs",
            request.method,
            request.url.path,
            response.status_code,
            cost
        )
        return response


def register_access_log_middleware(app: FastAPI):
    app.add_middleware(ExceptionHandlerMiddleware)
