import uuid
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.models.workspace import WorkspaceRole


class WorkspaceBase(BaseModel):
    name: str
    description: Optional[str] = None


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class WorkspaceMembers(BaseModel):
    id: uuid.UUID
    name: str
    role: WorkspaceRole


class WorkspaceResponse(WorkspaceBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    owner_id: uuid.UUID
    members: List[WorkspaceMembers] = []

# ------- Invite User to Workspace ----


class WorkspaceInviteRequest(BaseModel):
    email: str
    role: WorkspaceRole
