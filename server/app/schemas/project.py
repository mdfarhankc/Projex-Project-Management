import uuid
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

from app.models.project import ProjectStatus


class ProjectBase(BaseModel):
    workspace_id: uuid.UUID
    name: str
    description: Optional[str] = None
    status: ProjectStatus
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectMember(BaseModel):
    id: uuid.UUID
    full_name: str


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    members: List[ProjectMember] = []
