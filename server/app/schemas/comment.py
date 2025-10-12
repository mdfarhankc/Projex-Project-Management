import uuid
from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str
    author_id: uuid.UUID
    task_id: uuid.UUID


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: uuid.UUID
