from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base class for all custom application exceptions."""

    def __init__(self,
                 detail: str = "An unexpected error occurred.",
                 status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)
