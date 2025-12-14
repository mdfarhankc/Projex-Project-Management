import uuid
from sqlmodel import Session, select
from typing import List

from app.models.project import Project
from app.schemas.project import ProjectCreate


def create_project_service(*, session: Session, project_create: ProjectCreate, user_id: uuid.UUID) -> Project:
    """ Create a new project with owner as loggedin user. """
    project_obj = Project.model_validate(
        project_create,
        update={"owner_id": user_id},
    )
    session.add(project_obj)
    session.commit()
    session.refresh(project_obj)
    return project_obj


def get_project_details_by_id(*, session: Session, project_id: uuid.UUID) -> Project | None:
    """ Get Project details by project_id """
    return session.get(Project, project_id)


def check_project_name_exists_for_workspace(*, session: Session, workspace_id: uuid.UUID, project_name: str) -> bool:
    """ Check if project with this name already exists in the workspace. """
    project = session.exec(
        select(Project)
        .where(
            Project.workspace_id == workspace_id,
            Project.name == project_name
        )
    ).first()
    return True if project else False


def get_all_workspace_projects(*, session: Session, workspace_id: uuid.UUID) -> List[Project]:
    """ Get all projects in the given workspace id. """
    return session.exec(
        select(Project).where(Project.workspace_id == workspace_id)
    )
