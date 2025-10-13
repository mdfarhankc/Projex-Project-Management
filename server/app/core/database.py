from fastapi import Depends
from sqlmodel import create_engine, Session
from typing import Annotated
from collections.abc import Generator
from redis import Redis

from app.core.config import settings

# -----------------
# --- Database ----
# -----------------
engine = create_engine(settings.DATABASE_URL)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


# -----------------
# --- Redis -------
# -----------------
redis_client = Redis.from_url(settings.REDIS_URL)


def get_redis() -> Redis:
    return redis_client


RedisDep = Annotated[Redis, Depends(get_redis)]
