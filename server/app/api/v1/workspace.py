import uuid
from fastapi import APIRouter, status
from typing import List

from app.core.database import SessionDep
from app.api.deps import CurrentUser
from app.services import workspace_service
from app.schemas.workspace import (
    WorkspaceResponse,
    WorkspaceCreate,
    WorkspaceUpdate,
    WorkspaceInviteRequest)
from app.exceptions.workspace import WorkspaceAlreadyExistException, WorkspaceNotFoundException

router = APIRouter(tags=["Workspace"])


@router.post("/",
             response_model=WorkspaceResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Create a new workspace")
def workspace_create_api(session: SessionDep, workspace_create: WorkspaceCreate, current_user: CurrentUser):
    workspace_exist = workspace_service.check_workspace_exists_for_user(
        session=session, user_id=current_user.id, workspace_name=workspace_create.name)
    if workspace_exist:
        raise WorkspaceAlreadyExistException()
    workspace = workspace_service.create_workspace_service(
        session=session, workspace_create=workspace_create, user_id=current_user.id)
    return workspace


@router.get("/",
            response_model=List[WorkspaceResponse],
            status_code=status.HTTP_200_OK,
            summary="Get User Workspaces - Owned and Member")
def workspace_get_api(session: SessionDep, current_user: CurrentUser):
    workspaces = workspace_service.get_user_workspaces(
        session=session, user_id=current_user.id)
    return workspaces


@router.get("/{workspace_id}/",
            response_model=WorkspaceResponse,
            status_code=status.HTTP_200_OK,
            summary="Get Workspace Details")
def workspace_get_details_api(session: SessionDep, workspace_id: str, current_user: CurrentUser):
    workspace = workspace_service.get_workspace_service(
        session=session, workspace_id=uuid.UUID(workspace_id))
    if workspace is None:
        raise WorkspaceNotFoundException()
    return workspace


@router.put("/{workspace_id}/",
            response_model=WorkspaceResponse,
            status_code=status.HTTP_200_OK,
            summary="Update workspace details")
def workspace_update_api(
    workspace_id: str,
    workspace_update: WorkspaceUpdate,
    session: SessionDep,
    current_user: CurrentUser
):
    # First, get the current workspace
    workspace = workspace_service.get_workspace_service(
        session=session, workspace_id=uuid.UUID(workspace_id)
    )
    if not workspace:
        raise WorkspaceNotFoundException(detail="Workspace not found")

    # Only check duplicate if name is changing
    if workspace_update.name and workspace_update.name != workspace.name:
        workspace_exist = workspace_service.check_workspace_exists_for_user(
            session=session, user_id=current_user.id, workspace_name=workspace_update.name
        )
        if workspace_exist:
            raise WorkspaceAlreadyExistException(
                detail="You already have a workspace with this name"
            )

    updated_workspace = workspace_service.update_workspace_service(
        session=session,
        workspace_id=uuid.UUID(workspace_id),
        workspace_update=workspace_update,
        user_id=current_user.id
    )

    if not updated_workspace:
        raise WorkspaceNotFoundException(
            detail="Workspace not found or not allowed to update")

    return updated_workspace


@router.delete("/{workspace_id}/",
               status_code=status.HTTP_200_OK,
               summary="Delete workspace by id")
def workspace_delete_api(session: SessionDep, workspace_id: str):
    delete_workspace = workspace_service.delete_workspace_service(
        session=session, workspace_id=uuid.UUID(workspace_id))
    if delete_workspace:
        return {"message": "Workspace deleted successfully!"}
    return {"error": "Failed to delete workspace", "status_code": status.HTTP_400_BAD_REQUEST}


@router.post("/{workspace_id}/invite/",
             status_code=status.HTTP_200_OK,
             summary="Invite user to workspace")
def workspace_invite_user_api(session: SessionDep, workspace_invite: WorkspaceInviteRequest, current_user: CurrentUser):
    pass
