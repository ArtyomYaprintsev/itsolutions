from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


class CustomException(Exception):
    """Application base exception class."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def exception_handler(request: Request, exc: CustomException):  # noqa: W0613
    """Base exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.message},
    )


class UnauthorizedException(HTTPException):
    """Raised when user is unauthenticated."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )


class UniqueException(CustomException):
    """Raised when detects duplicate."""

    def __init__(self, message: str):
        super().__init__(message)


class InvalidCredentialsException(CustomException):
    """Raised when provided invalid credentials."""

    def __init__(self):
        super().__init__('Invalid credentials')


class InactiveUserException(CustomException):
    """Raised when user is inactive."""

    def __init__(self):
        super().__init__('User is inactive')


class NotSuperuserException(CustomException):
    """Raised when user is not superuser."""

    def __init__(self):
        super().__init__('User is not superuser')


class AdNotFoundException(CustomException):
    """Raised when Ad not found."""

    def __init__(self):
        super().__init__(
            message='Ad not found',
            status_code=status.HTTP_404_NOT_FOUND,
        )


class ArchivedAdException(CustomException):
    """Raised when Ad is archived."""

    def __init__(self):
        super().__init__(
            message='Ad is archived',
            status_code=status.HTTP_403_FORBIDDEN,
        )
