from fastapi import status
from fastapi.testclient import TestClient
from app.core.config import settings
from app.tests.api.deps import *


# ------------ Deps -----------
@pytest.fixture
def tag_data() -> dict[str, str]:
    return {
        "name": "Test Tag",
        "color_hex": "#ff44gg"
    }


@pytest.fixture
def create_tag(auth_client: TestClient, tag_data: dict[str, str]) -> dict[str, str]:
    response = auth_client.post(
        f"{settings.API_V1_STR}/tags/", json=tag_data)
    data = response.json()
    return {**tag_data, "id": data['id']}


# ------ Create Tag API Tests -----------
def test_tag_create_new_tag_api_success(auth_client: TestClient, tag_data: dict[str, str]):
    response = auth_client.post(
        f"{settings.API_V1_STR}/tags/", json=tag_data)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["name"] == tag_data["name"]
    assert data["color_hex"] == tag_data["color_hex"]


def test_tag_create_new_tag_api_tag_exists(auth_client: TestClient, tag_data: dict[str, str]):
    auth_client.post(
        f"{settings.API_V1_STR}/tags/", json=tag_data)
    response = auth_client.post(
        f"{settings.API_V1_STR}/tags/", json=tag_data)

    assert response.status_code == status.HTTP_409_CONFLICT


def test_tag_create_new_tag_api_fields_missing(auth_client: TestClient):
    response = auth_client.post(f"{settings.API_V1_STR}/tags/")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
