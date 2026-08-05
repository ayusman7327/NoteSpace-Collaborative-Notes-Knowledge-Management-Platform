from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse
)
from app.services.workspace_service import (
    create_new_workspace,
    list_user_workspaces
)


router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"]
)


@router.post(
    "",
    response_model=WorkspaceResponse
)
def create_workspace(
    workspace_data: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_new_workspace(
        db=db,
        workspace_data=workspace_data,
        user_id=current_user.id
    )


@router.get(
    "",
    response_model=list[WorkspaceResponse]
)
def get_workspaces(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return list_user_workspaces(
        db=db,
        user_id=current_user.id
    )