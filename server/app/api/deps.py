from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from app.core.config import settings
from app.core.database import SessionDep
from app.core.security import decode_access_token
from app.models.user import User
from app.exceptions.user import InactiveUserException, UserNotFoundException, UnAuthorizedException

# OAuth2 reusable token dependency
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    refreshUrl=f"{settings.API_V1_STR}/auth/refresh",
    auto_error=False,
)
TokenDep = Annotated[str, Depends(reusable_oauth2)]


# -----------------------------
# Current User Dependency
# -----------------------------
def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """ Return the current authenticated user. """
    if token is None:
        raise UnAuthorizedException()
    user_id = decode_access_token(token=token)
    user = session.get(User, user_id)
    if not user:
        raise UserNotFoundException()
    if not user.is_active:
        raise InactiveUserException()
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
