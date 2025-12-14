import uuid
from sqlmodel import Session, select
from typing import List

from app.models.workspace import Workspace, WorkspaceMember
from app.schemas.workspace import WorkspaceCreate
from app.utils.workspace_slug import generate_unique_workspace_slug


def create_workspace_service(*, session: Session, workspace_create: WorkspaceCreate, user_id: uuid.UUID) -> Workspace:
    """ Create new workspace with owner as loggedin user. """
    slug = generate_unique_workspace_slug(
        session=session, base_name=workspace_create.name)
    workspace_obj = Workspace.model_validate(
        workspace_create,
        update={
            "owner_id": user_id,
            "slug": slug
        }
    )
    session.add(workspace_obj)
    session.commit()
    session.refresh(workspace_obj)
    return workspace_obj


def get_workspace_service(*, session: Session, workspace_id: uuid.UUID) -> Workspace | None:
    """ Get Workspace details by workspace id. """
    return session.get(Workspace, workspace_id)


def check_workspace_exists_for_user(*, session: Session, user_id: uuid.UUID, workspace_name: str) -> bool:
    """ Check if workspace with this name exist for the user. """
    owned_workspace = session.exec(
        select(Workspace)
        .where(
            Workspace.name == workspace_name,
            Workspace.owner_id == user_id
        )
    ).first()
    if owned_workspace:
        return True

    # Check if user is a member of any workspace with the same name
    member_workspace = session.exec(
        select(Workspace)
        .join(WorkspaceMember, Workspace.id == WorkspaceMember.workspace_id)
        .where(
            Workspace.name == workspace_name,
            WorkspaceMember.user_id == user_id,
        )
    ).first()

    return member_workspace is not None


def get_user_workspaces(*, session: Session, user_id: uuid.UUID) -> List[Workspace]:
    """ Get all workspaces owned by user or user is a member of the workspace """
    owned_workspaces = session.exec(
        select(Workspace).where(Workspace.owner_id == user_id)
    ).all()

    member_workspace_ids = session.exec(
        select(WorkspaceMember.workspace_id).where(
            WorkspaceMember.user_id == user_id)
    ).all()

    member_workspaces = []
    if member_workspace_ids:
        member_workspaces = session.exec(
            select(Workspace).where(Workspace.id.in_(member_workspace_ids))
        ).all()

    all_workspaces = {ws.id: ws for ws in owned_workspaces + member_workspaces}
    return list(all_workspaces.values())


def update_workspace_service(*, session: Session, workspace_id: uuid.UUID, workspace_update: WorkspaceCreate, user_id: uuid.UUID) -> Workspace | None:
    """ Update workspace (only if user is the owner). Auto-updates slug if name is changed."""
    workspace = get_workspace_service(
        session=session, workspace_id=workspace_id)

    if workspace is None:
        return None

    if workspace.owner_id != user_id:
        return None

    # If name changed, regenerate slug
    if workspace_update.name and workspace_update.name != workspace.name:
        workspace.slug = generate_unique_workspace_slug(
            session=session, base_name=workspace_update.name
        )
        workspace.name = workspace_update.name

    # Update other fields
    if workspace_update.description is not None:
        workspace.description = workspace_update.description

    session.add(workspace)
    session.commit()
    session.refresh(workspace)
    return workspace


def delete_workspace_service(*, session: Session, workspace_id: uuid.UUID) -> bool:
    """ Delete workspace by id. """
    workspace = get_workspace_service(
        session=session, workspace_id=workspace_id)
    if workspace is None:
        return False
    session.delete(workspace)
    session.commit()
    return True


# -----------------------------------
def create_default_workspace_for_user(*, session: Session, user_id: uuid.UUID, user_name: str) -> Workspace:
    """ Create personal workspace for the given user as - User's Workspace. """
    workspace_create = WorkspaceCreate(
        name=f"{user_name}'s Workspace",
        description=f"{user_name}'s Personal Workspace",
    )
    workspace_obj = create_workspace_service(
        session=session,
        workspace_create=workspace_create,
        user_id=user_id,
    )
    return workspace_obj
