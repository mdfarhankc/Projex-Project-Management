import uuid
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.task import Task


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    content: str
    is_edited: bool = Field(default=False)

    # Timestamp fields
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    # Author - Many2one
    author_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    author: "User" = Relationship()

    # Task - Many2one
    task_id: uuid.UUID = Field(foreign_key="tasks.id", index=True)
    task: "Task" = Relationship(back_populates="comments")
