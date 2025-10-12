import uuid
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING

from app.models.workspace import WorkspaceMember
from app.models.project import ProjectMember

if TYPE_CHECKING:
    from app.models.workspace import Workspace
    from app.models.project import Project
    from app.models.task import Task


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    full_name: str = Field(nullable=False, max_length=255)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    # Timestamp fields
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    last_login_at: Optional[datetime] = None

    # Owned Projects - One2many
    owned_projects: List["Project"] = Relationship(back_populates="owner")

    # Member of Workspaces - Many2many
    workspaces: List["Workspace"] = Relationship(
        back_populates="members",
        link_model=WorkspaceMember
    )

    # Member of Projects - Many2many
    member_projects: List["Project"] = Relationship(
        back_populates="members",
        link_model=ProjectMember
    )

    # User tasks - One2many
    tasks: List["Task"] = Relationship(back_populates="owner")
