from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.base import AppException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exception: AppException):
        return JSONResponse(
            status_code=exception.status_code,
            content={
                "error": exception.detail,
                "status_code": exception.status_code,
            },
        )
