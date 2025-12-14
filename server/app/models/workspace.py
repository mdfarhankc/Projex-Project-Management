import uuid
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone, timedelta
from typing import Optional, List, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.project import Project


class WorkspaceRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


# Link table for Many-to-Many relationship between Workspace and User
class WorkspaceMember(SQLModel, table=True):
    __tablename__ = "workspace_members"

    workspace_id: uuid.UUID = Field(
        foreign_key="workspaces.id", primary_key=True, index=True)
    user_id: uuid.UUID = Field(
        foreign_key="users.id", primary_key=True, index=True)
    role: WorkspaceRole = Field(default=WorkspaceRole.MEMBER)
    joined_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))


class Workspace(SQLModel, table=True):
    __tablename__ = "workspaces"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(nullable=False, max_length=100)
    slug: str = Field(nullable=False, unique=True, index=True)
    description: Optional[str] = None

    # Timestamp fields
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    # Owner (workspace creator) - Many2one
    owner_id: uuid.UUID = Field(
        foreign_key="users.id", nullable=False, index=True)
    owner: "User" = Relationship()

    # Projects in workspace - One2many
    projects: List["Project"] = Relationship(back_populates="workspace")

    # Members in workspace - Many2many
    members: List["User"] = Relationship(
        back_populates="workspaces",
        link_model=WorkspaceMember
    )

    # Invitations - One2Many
    invitations: List["WorkspaceInvitation"] = Relationship()


class WorkspaceInvitationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"
    EXPIRED = "expired"


class WorkspaceInvitation(SQLModel, table=True):
    __tablename__ = "workspace_invitations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    role: WorkspaceRole = Field(default=WorkspaceRole.MEMBER)
    status: WorkspaceInvitationStatus = Field(
        default=WorkspaceInvitationStatus.PENDING)

    # Workspace, Inviter and Invitee ids
    workspace_id: uuid.UUID = Field(foreign_key="workspaces.id")
    inviter_id: uuid.UUID = Field(foreign_key="users.id")
    invitee_id: uuid.UUID = Field(foreign_key="users.id")

    # Dates
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=7))
