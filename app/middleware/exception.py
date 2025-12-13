from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.utils.response import APIResponse


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            return await call_next(request)
        except HTTPException as e:
            print(e)
            return JSONResponse(APIResponse.error(message=str(e.detail), code=e.status_code), status_code=e.status_code)
        except RequestValidationError as e:
            print(e.errors())
            return JSONResponse(APIResponse.error(message="validation error", code=422, data=e.errors()),
                                status_code=422)
        except Exception as e:
            print(e)
            return JSONResponse(APIResponse.error(message=f"internal error:{e}", code=500), status_code=500)


def register_exception_middleware(app: FastAPI):
    app.add_middleware(ExceptionHandlerMiddleware)
