from fastapi import status
from app.exceptions.base import AppException


class UnAuthorizedException(AppException):
    def __init__(self, detail: str = "Authorization token missing"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


class IncorrectCredsException(AppException):
    def __init__(self, detail: str = "Incorrect email or password!"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class UserNotFoundException(AppException):
    def __init__(self, detail: str = "User not found!"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class InactiveUserException(AppException):
    def __init__(self, detail: str = "Inactive user!"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class UserAlreadyExistException(AppException):
    def __init__(self, detail: str = "User with this email already exists."):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )
