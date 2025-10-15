import pytest
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
