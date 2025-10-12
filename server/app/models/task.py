import uuid
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from enum import Enum

from app.models.tag import TaskTag

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.timesheet import Timesheet
    from app.models.comment import Comment
    from app.models.tag import Tag


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatus(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    CANCELLED = "cancelled"


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=300, index=True)
    description: Optional[str] = None
    is_archived: bool = Field(default=False)

    # Enum fields
    status: TaskStatus = Field(default=TaskStatus.DRAFT, index=True)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, index=True)
    
    # Task progress
    estimated_hours: Optional[float] = Field(default=None, ge=0)
    actual_hours: Optional[float] = Field(default=None, ge=0)
    progress_percentage: int = Field(default=0, ge=0, le=100)

    # Timestamp fields
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    # Owner - Many2one
    owner_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    owner: "User" = Relationship(back_populates="tasks")

    # Timesheets - One2many
    timesheets: list["Timesheet"] = Relationship(back_populates="task")

    # Comments - One2many
    comments: list["Comment"] = Relationship(back_populates="task")

    # Tags - Many2many
    tags: List["Tag"] = Relationship(
        back_populates="tasks", link_model=TaskTag)
