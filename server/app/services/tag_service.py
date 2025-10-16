import uuid
from sqlmodel import Session, select
from typing import Optional, List

from app.models.tag import Tag
from app.schemas.tag import (
    TagCreate
)


def create_new_tag(*, session: Session, tag_create: TagCreate) -> Tag:
    tag_obj = Tag.model_validate(tag_create)
    session.add(tag_obj)
    session.commit()
    session.refresh(tag_obj)
    return tag_obj


def get_tag_by_id(*, session: Session, tag_id: uuid.UUID) -> Tag | None:
    tag = session.exec(
        select(Tag).where(Tag.id == tag_id)
    ).first()
    return tag


def get_tag_by_name(*, session: Session, tag_name: uuid.UUID) -> Tag | None:
    tag = session.exec(
        select(Tag).where(Tag.name == tag_name)
    ).first()
    return tag


def search_tags(*, session: Session, query: Optional[str] = None) -> List[Tag]:
    stmt = select(Tag)
    if query:
        stmt = stmt.where(Tag.name.ilike(f"%{query}%"))
    tags = session.exec(stmt).all()
    return tags
