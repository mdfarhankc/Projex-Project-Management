from fastapi import status
from app.exceptions.base import AppException


class TagAlreadyExistException(AppException):
    def __init__(self, detail: str = "Tag with this name already exists!"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )
