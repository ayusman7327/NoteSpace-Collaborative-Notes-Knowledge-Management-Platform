from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse,
    WorkspaceUpdate,
)
from app.services.workspace_service import (
    create_workspace,
    delete_workspace,
    get_user_workspaces,
    get_workspace,
    update_workspace,
)


router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"],
)


@router.post(
    "",
    response_model=WorkspaceResponse,
)
def create_workspace_route(
    data: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_workspace(
        db=db,
        user_id=current_user.id,
        workspace_data=data,
    )


@router.get(
    "",
    response_model=list[WorkspaceResponse],
)
def get_workspaces_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_workspaces(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def get_workspace_route(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_workspace(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )


@router.patch(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def update_workspace_route(
    workspace_id: int,
    data: WorkspaceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_workspace(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
        workspace_data=data,
    )


@router.delete(
    "/{workspace_id}",
)
def delete_workspace_route(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_workspace(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )