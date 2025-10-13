import uuid
from redis import Redis


def store_refresh_token_in_redis(*, redis: Redis, user_id: uuid.UUID, token: str, expiry_days: int = 7) -> None:
    redis.setex(
        f"refresh_token:{user_id}",
        expiry_days * 24 * 60 * 60,
        token
    )


def get_refresh_token_from_redis(*, redis: Redis, user_id: uuid.UUID) -> str | None:
    token = redis.get(f"refresh_token:{user_id}")
    return token.decode() if token else None


def delete_refresh_token_from_Redis(*, redis: Redis, user_id: uuid.UUID) -> None:
    redis.delete(f"refresh_token:{user_id}")
