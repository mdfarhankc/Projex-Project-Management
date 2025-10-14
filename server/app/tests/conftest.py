import pytest
import fakeredis
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool


from app.main import app
from app.core.database import get_db, get_redis
from app.models import *


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    # Create a fake Redis instance
    fake_redis = fakeredis.FakeStrictRedis()

    # Override Redis dependency
    def get_redis_override():
        return fake_redis

    app.dependency_overrides[get_db] = get_session_override
    app.dependency_overrides[get_redis] = get_redis_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
