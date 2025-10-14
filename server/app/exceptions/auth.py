from fastapi import status
from app.exceptions.base import AppException


class InvalidTokenException(AppException):
    def __init__(self, detail: str = "Invalid or expired token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
