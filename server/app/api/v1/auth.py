from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.core.database import SessionDep, RedisDep
from app.core.security import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from app.services import user_service
from app.services import redis_service
from app.exceptions.user import UserAlreadyExistException, UnAuthorizedException, InactiveUserException
from app.schemas.auth import (
    UserCreate,
    RegisterResponse,
    LoginResponse,
    RefreshTokenResponse,
    LogoutSchema,
)

router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def auth_register(session: SessionDep, register_user: UserCreate):
    user = user_service.get_user_by_email(
        session=session, email=register_user.email)
    if user:
        raise UserAlreadyExistException()
    new_user = user_service.create_new_user(
        session=session, user_create=register_user)
    return new_user


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def auth_login(session: SessionDep, redis: RedisDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = user_service.authenticate_user(
        session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise UnAuthorizedException()
    if not user.is_active:
        raise InactiveUserException()

    # Create access and refresh token
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    #  Store refresh token in redis for 7 days
    redis_service.store_refresh_token_in_redis(
        redis=redis, user_id=user.id, token=refresh_token)
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user,
    )


@router.post("/refresh", response_model=RefreshTokenResponse, status_code=status.HTTP_200_OK)
def auth_token_refresh():
    pass


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def auth_logout(logout_schema: LogoutSchema, redis: RedisDep):
    user_id = decode_refresh_token(token=logout_schema.refresh_token)
    print(user_id)
    redis_service.delete_refresh_token_from_Redis(redis=redis, user_id=user_id)
