from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Any, Annotated
from passlib.context import CryptContext

from app.core.config import settings
from app.core.database import SessionDep
from app.models.user import User
from app.exceptions.user import InactiveUserException, UserNotFoundException
from app.exceptions.auth import InvalidTokenException

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# OAuth2 reusable token dependency
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)
TokenDep = Annotated[str, Depends(reusable_oauth2)]


# -----------------------------
# Password Utilities
# -----------------------------
def get_password_hash(*, password: str) -> str:
    """ Return the hashed password ."""
    return pwd_context.hash(password)


def verify_password(*, plain_password: str, hashed_password: str) -> bool:
    """ Verify the hashed password is correct or not ."""
    return pwd_context.verify(plain_password, hashed_password)


# -----------------------------
# Token Utilities
# -----------------------------
def create_access_token(*, subject: str | Any, expire_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    """ Create access token with 30 minutes expiry as default. """
    expire = datetime.now(timezone.utc) + expire_delta
    payload = {"exp": expire, "sub": str(subject)}
    return jwt.encode(payload, settings.TOKEN_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)


def create_refresh_token(*, subject: str | Any, expire_delta: timedelta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)) -> str:
    """ Create refresh token with 7 days expiry as default. """
    expire = datetime.now(timezone.utc) + expire_delta
    payload = {"exp": expire, "sub": str(subject), "type": "refresh"}
    return jwt.encode(payload, settings.TOKEN_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)


def decode_access_token(*, token: str) -> str | Any:
    """ Decode access token and return subject (user_id/email). """
    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[
                             settings.TOKEN_ALGORITHM])
        return payload['sub']
    except JWTError:
        raise InvalidTokenException()


def decode_refresh_token(*, token: str) -> str | Any:
    """ Decode refresh token and return subject (user_id/email). """
    try:
        payload = jwt.decode(
            token,
            settings.TOKEN_SECRET_KEY,
            algorithms=[settings.TOKEN_ALGORITHM]
        )
        # Ensure the token type is refresh
        if payload.get("type") != "refresh":
            raise InvalidTokenException()
        return payload["sub"]
    except JWTError:
        raise InvalidTokenException()


# -----------------------------
# Current User Dependency
# -----------------------------
def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """ Return the current authenticated user. """
    user_id = decode_access_token(token=token)
    user = session.get(User, user_id)
    if not user:
        raise UserNotFoundException()
    if not user.is_active:
        raise InactiveUserException()
    return user
