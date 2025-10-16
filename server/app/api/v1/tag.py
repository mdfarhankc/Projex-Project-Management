from fastapi import APIRouter, Query, status
from typing import List, Optional

from app.core.database import SessionDep
from app.services import tag_service
from app.schemas.tag import (
    TagCreate,
    TagResponse
)
from app.exceptions.tag import TagAlreadyExistException
from app.api.deps import CurrentUser

router = APIRouter(tags=["Tag"])


@router.post(
    "/",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new tag")
def tag_create_new_tag(session: SessionDep, tag_create: TagCreate, current_user: CurrentUser):
    tag = tag_service.get_tag_by_name(
        session=session, tag_name=tag_create.name)
    if tag:
        raise TagAlreadyExistException()
    new_tag = tag_service.create_new_tag(
        session=session, tag_create=tag_create)
    return new_tag


@router.get(
    "/search/",
    response_model=List[TagResponse],
    status_code=status.HTTP_200_OK,
    summary="Search tags by query"
)
def search_tags(
    session: SessionDep,
    q: Optional[str] = Query(default=None, description="Search query"),
    current_user: CurrentUser = None
):
    tags = tag_service.search_tags(session=session, query=q)
    return tags
