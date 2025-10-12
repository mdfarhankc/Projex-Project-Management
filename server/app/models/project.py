import uuid
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.workspace import Workspace


class ProjectStatus(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    ARCHIVED = "archived"


# Link table for Many-to-Many relationship between Project and User
class ProjectMember(SQLModel, table=True):
    __tablename__ = "project_members"

    project_id: uuid.UUID = Field(foreign_key="projects.id", primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True)
    joined_at: datetime = Field(default_factory=datetime.now(timezone.utc))


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(nullable=False, max_length=255)
    description: Optional[str] = None
    status: ProjectStatus = Field(default=ProjectStatus.PLANNING, index=True)

    # Timestamp fields
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    # Project Owner - Many2one
    owner_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    owner: "User" = Relationship(back_populates="owned_projects")

    # Workspace of the project - Many2one
    workspace_id: uuid.UUID = Field(
        foreign_key="workspaces.id", nullable=False, index=True)
    workspace: "Workspace" = Relationship(back_populates="projects")

    # Project Members - Many2Many
    members: List["User"] = Relationship(
        back_populates="member_projects",
        link_model=ProjectMember
    )
