import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings


@pytest.fixture
def user_data() -> dict[str, str]:
    return {
        "full_name": settings.FIRST_SUPERUSER_NAME,
        "email": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }


@pytest.fixture
def create_user(client: TestClient, user_data: dict) -> dict:
    # Try registering the user; ignore if already exists
    client.post(f"{settings.API_V1_STR}/auth/register", json=user_data)
    return user_data


@pytest.fixture
def access_token(client: TestClient, create_user) -> str:
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": create_user["email"],
            "password": create_user["password"]
        }
    )
    token = response.json().get("access_token")
    return token


@pytest.fixture
def refresh_token(client: TestClient, create_user) -> str:
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": create_user["email"],
            "password": create_user["password"]
        }
    )
    token = response.json().get("refresh_token")
    return token


@pytest.fixture
def auth_client(client: TestClient, access_token: str) -> TestClient:
    """TestClient with Authorization header pre-set."""
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client


# ------ Register API Tests -----------
def test_auth_register_success(client: TestClient, user_data: dict[str, str]):
    response = client.post(
        f"{settings.API_V1_STR}/auth/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "password" not in data


def test_auth_register_user_exists(client: TestClient, user_data: dict[str, str]):
    client.post(
        f"{settings.API_V1_STR}/auth/register", json=user_data)
    response = client.post(
        f"{settings.API_V1_STR}/auth/register", json=user_data)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_auth_register_missing_fields(client: TestClient, user_data: dict[str, str]):
    response = client.post(
        f"{settings.API_V1_STR}/auth/register", json={
            "full_name": user_data["full_name"]
        })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# ------ Login API Tests -----------
def test_auth_login_success(client: TestClient, create_user: dict):
    response = client.post(
        f"{settings.API_V1_STR}/auth/login", data={
            "username": create_user["email"],
            "password": create_user["password"]
        })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "user" in data


def test_auth_login_user_not_found(client: TestClient, user_data: dict[str, str]):
    response = client.post(
        f"{settings.API_V1_STR}/auth/login", data={
            "username": user_data["email"],
            "password": user_data["password"]
        })
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_auth_login_missing_fields(client: TestClient, user_data: dict[str, str]):
    response = client.post(
        f"{settings.API_V1_STR}/auth/login", data={
            "username": user_data["email"],
        })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# --------- Current User API Tests -------
def test_auth_current_user_success(auth_client: TestClient):
    response = auth_client.get(f"{settings.API_V1_STR}/auth/me")
    assert response.status_code == status.HTTP_200_OK


def test_auth_current_user_no_token(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_auth_current_user_invalid_token(client: TestClient):
    client.headers.update({"Authorization": "Bearer invalidtoken"})
    response = client.get(f"{settings.API_V1_STR}/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ------ Refresh Token API Tests ----------------
def test_refresh_token_success(client: TestClient, refresh_token: str):
    response = client.post(f"{settings.API_V1_STR}/auth/refresh",
                           json={"refresh_token": refresh_token})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_refresh_token_no_token(client: TestClient):
    response = client.post(f"{settings.API_V1_STR}/auth/refresh")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_refresh_token_invalid_token(client: TestClient):
    response = client.post(f"{settings.API_V1_STR}/auth/refresh",
                           json={"refresh_token": "invalidtoken"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ------ Logout API Tests ----------------
def test_auth_logout_success(client: TestClient, refresh_token: str):
    response = client.post(f"{settings.API_V1_STR}/auth/logout",
                           json={"refresh_token": refresh_token})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_auth_logout_no_token(client: TestClient):
    response = client.post(f"{settings.API_V1_STR}/auth/logout")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_auth_logout_invalid_token(client: TestClient):
    response = client.post(f"{settings.API_V1_STR}/auth/logout",
                           json={"refresh_token": "invalidtoken"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
