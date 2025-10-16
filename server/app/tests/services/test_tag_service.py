import pytest
import uuid
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.tag import TagCreate
from app.services.tag_service import (
    create_new_tag,
    get_tag_by_id,
    get_tag_by_name,
    search_tags
)


# --------- Deps ---------------
@pytest.fixture
def tag_data() -> dict[str, str]:
    return {
        "name": "Test Tag",
        "color_hex": "#ff44gg"
    }


@pytest.fixture
def create_tag(session: Session, tag_data: dict[str, str]) -> dict[str, str]:
    tag_create = TagCreate(**tag_data)
    tag = create_new_tag(session=session, tag_create=tag_create)
    return {**tag_data, "id": tag.id}


# ---------- Create new tag service tests -------------
def test_create_new_tag_success(session: Session, tag_data: dict[str, str]):
    tag_create = TagCreate(**tag_data)
    tag = create_new_tag(session=session, tag_create=tag_create)

    assert tag.id is not None
    assert tag.name == tag_data["name"]
    assert tag.color_hex == tag_data["color_hex"]


def test_create_new_tag_tag_exists(session: Session, tag_data: dict[str, str]):
    tag_create = TagCreate(**tag_data)
    create_new_tag(session=session, tag_create=tag_create)

    with pytest.raises(IntegrityError):
        create_new_tag(session=session, tag_create=tag_create)


# ---------- Get tag by id service tests -------------
def test_get_tag_by_id_tag_found(session: Session, create_tag: dict[str, str]):
    tag = get_tag_by_id(session=session, tag_id=create_tag['id'])

    assert tag is not None
    assert tag.id == create_tag["id"]
    assert tag.name == create_tag["name"]


def test_get_tag_by_id_tag_not_found(session: Session):
    tag = get_tag_by_id(session=session, tag_id=uuid.uuid4())

    assert tag is None


# ---------- Get tag by name service tests -------------
def test_get_tag_by_name_tag_found(session: Session, create_tag: dict[str, str]):
    tag = get_tag_by_name(session=session, tag_name=create_tag['name'])

    assert tag is not None
    assert tag.id == create_tag["id"]
    assert tag.name == create_tag["name"]


def test_get_tag_by_name_tag_not_found(session: Session):
    tag = get_tag_by_name(session=session, tag_name="Not found")

    assert tag is None


def test_search_tags_success(session: Session, create_tag: dict[str, str]):
    tags = search_tags(session=session, query=create_tag['name'])

    assert len(tags) > 0


def test_search_tags_not_found(session: Session):
    tags = search_tags(session=session, query="Not found")

    assert len(tags) == 0
