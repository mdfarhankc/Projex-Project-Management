import pytest
import uuid
import fakeredis
from redis import Redis
from datetime import timedelta
from app.core.config import settings
from app.services.redis_service import (
    store_refresh_token_in_redis,
    get_refresh_token_from_redis,
    delete_refresh_token_from_Redis,
)


@pytest.fixture
def redis_client():
    """Return a fake Redis instance for testing."""
    return fakeredis.FakeRedis()


def test_store_refresh_token_in_redis(redis_client: Redis):
    user_id = uuid.uuid4()
    token = "sample_refresh_token"

    store_refresh_token_in_redis(
        redis=redis_client, user_id=user_id, token=token)
    stored_value = redis_client.get(f"refresh_token:{user_id}")
    assert stored_value is not None
    assert stored_value.decode() == token


def test_get_refresh_token_in_redis(redis_client: Redis):
    user_id = uuid.uuid4()
    token = "sample_refresh_token"

    redis_client.setex(f"refresh_token:{user_id}", timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS), token)
    saved_token = get_refresh_token_from_redis(
        redis=redis_client, user_id=user_id)
    assert saved_token == token


def test_delete_refresh_token(redis_client):
    user_id = uuid.uuid4()
    token = "sample_refresh_token"
    # store first
    store_refresh_token_in_redis(
        redis=redis_client, user_id=user_id, token=token)
    assert get_refresh_token_from_redis(
        redis=redis_client, user_id=user_id) == token
    # delete
    delete_refresh_token_from_Redis(redis=redis_client, user_id=user_id)
    assert get_refresh_token_from_redis(
        redis=redis_client, user_id=user_id) is None


def test_store_token_expiry(redis_client):
    user_id = uuid.uuid4()
    token = "sample_refresh_token"

    store_refresh_token_in_redis(
        redis=redis_client, user_id=user_id, token=token, expiry_days=2)

    ttl = redis_client.ttl(f"refresh_token:{user_id}")
    # TTL should be roughly equal to 2 days in seconds (allowing a small margin)
    assert 172000 <= ttl <= 173000
