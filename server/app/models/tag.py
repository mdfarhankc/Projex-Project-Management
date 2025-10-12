import uuid
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task


# Link table for Many-to-Many relationship between Task and Tag
class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tags"

    task_id: uuid.UUID = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: uuid.UUID = Field(foreign_key="tags.id", primary_key=True)


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=50)
    color_hex: Optional[str] = Field(default="#3B82F6", max_length=7)

    # Tasks - Many2many
    tasks: list["Task"] = Relationship(
        back_populates="tags",
        link_model=TaskTag
    )
