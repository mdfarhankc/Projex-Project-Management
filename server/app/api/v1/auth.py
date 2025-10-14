from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.api.deps import CurrentUser
from app.core.database import SessionDep, RedisDep
from app.core.security import create_access_token, create_refresh_token, decode_refresh_token
from app.services import user_service, redis_service
from app.exceptions.auth import InvalidTokenException
from app.exceptions.user import UserAlreadyExistException, IncorrectCredsException, InactiveUserException
from app.schemas.auth import (
    UserCreate,
    RegisterResponse,
    LoginResponse,
    CurrentUserResponse,
    RefreshTokenSchema,
    RefreshTokenResponse,
    LogoutSchema,
)

router = APIRouter(tags=["Auth"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user with email and password.")
def auth_register(session: SessionDep, register_user: UserCreate):
    user = user_service.get_user_by_email(
        session=session, email=register_user.email)
    if user:
        raise UserAlreadyExistException()
    new_user = user_service.create_new_user(
        session=session, user_create=register_user)
    return new_user


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Login the user using email and password.")
def auth_login(session: SessionDep, redis: RedisDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = user_service.authenticate_user(
        session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise IncorrectCredsException()
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


@router.get(
    "/me",
    response_model=CurrentUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current logged in user.")
def auth_current_user(current_user: CurrentUser):
    return current_user


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh and get the new access token.")
def auth_token_refresh(refresh_schema: RefreshTokenSchema, redis: RedisDep):
    user_id = decode_refresh_token(token=refresh_schema.refresh_token)

    # Get stored refresh token from Redis
    stored_token = redis_service.get_refresh_token_from_redis(
        redis=redis, user_id=user_id)

    # Check token validity
    if not stored_token or stored_token != refresh_schema.refresh_token:
        raise InvalidTokenException(
            detail="Refresh token is invalid or expired.")

    # Delete old refresh token
    redis_service.delete_refresh_token_from_Redis(redis=redis, user_id=user_id)

    # Create new access and refresh token
    access_token = create_access_token(subject=user_id)
    refresh_token = create_refresh_token(subject=user_id)

    #  Store new refresh token in redis for 7 days
    redis_service.store_refresh_token_in_redis(
        redis=redis, user_id=user_id, token=refresh_token)
    return RefreshTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout user.")
def auth_logout(logout_schema: LogoutSchema, redis: RedisDep):
    user_id = decode_refresh_token(token=logout_schema.refresh_token)
    redis_service.delete_refresh_token_from_Redis(redis=redis, user_id=user_id)
