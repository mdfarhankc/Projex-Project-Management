import pytest
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.auth import UserCreate
from app.services.user_service import (
    get_user_by_email,
    create_new_user,
    authenticate_user
)
from app.tests.api.deps import *


# ---------- Create new user service tests -------------
def test_create_new_user(session: Session, user_data: dict[str, str]):
    user_create = UserCreate(**user_data)
    user = create_new_user(session=session, user_create=user_create)

    assert user.id is not None
    assert user.email == user_data["email"]
    assert user.hashed_password != user_data["password"]


def test_create_new_user_user_exists(session: Session, user_data: dict[str, str]):
    user_create = UserCreate(**user_data)
    create_new_user(session=session, user_create=user_create)

    with pytest.raises(IntegrityError):
        create_new_user(session=session, user_create=user_create)


# ---------- Get user data by email service tests -------------
def test_get_user_by_email(session: Session, user_data: dict[str, str]):
    user_create = UserCreate(**user_data)
    created_user = create_new_user(session=session, user_create=user_create)

    user = get_user_by_email(session=session, email=user_data["email"])
    assert user is not None
    assert user.id == created_user.id
    assert user.email == created_user.email


def test_get_user_by_email_not_found(session: Session):
    user = get_user_by_email(session=session, email="notfound@example.com")
    assert user is None


# ---------- Authenticate user service tests -------------
def test_authenticate_user_success(session: Session, user_data: dict[str, str]):
    user_create = UserCreate(**user_data)
    create_new_user(session=session, user_create=user_create)

    user = authenticate_user(
        session=session, email=user_data["email"], password=user_data["password"])
    assert user is not None
    assert user.email == user_data["email"]


def test_authenticate_user_invalid_password(session: Session, user_data: dict[str, str]):
    user_create = UserCreate(**user_data)
    create_new_user(session=session, user_create=user_create)

    user = authenticate_user(
        session=session, email=user_data["email"], password="wrongpassword")
    assert user is None


def test_authenticate_user_not_found(session: Session):
    user = authenticate_user(
        session=session, email="ghost@example.com", password="password")
    assert user is None
