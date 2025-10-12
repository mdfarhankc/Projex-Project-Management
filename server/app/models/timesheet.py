import uuid
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.task import Task


class Timesheet(SQLModel, table=True):
    __tablename__ = "timesheets"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    description: str = Field(nullable=False, max_length=255)
    hours: float = Field(gt=0, description="Number of hours logged")

    # Timestamp fields
    work_date: datetime = Field(default_factory=datetime.now(timezone.utc), index=True)
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    # User - Many2one
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    user: "User" = Relationship()

    # Task - Many2one
    task_id: uuid.UUID = Field(foreign_key="tasks.id", index=True)
    task: "Task" = Relationship(back_populates="timesheets")
