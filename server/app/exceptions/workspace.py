from fastapi import status
from app.exceptions.base import AppException


class WorkspaceAlreadyExistException(AppException):
    def __init__(self, detail: str = "Workspace with this name already exists for this user!"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class WorkspaceNotFoundException(AppException):
    def __init__(self, detail: str = "Workspace not found!"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )
