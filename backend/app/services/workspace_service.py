from sqlalchemy.orm import Session

from app.repositories.workspace_repository import (
    create_workspace,
    get_user_workspaces
)
from app.schemas.workspace import WorkspaceCreate


def create_new_workspace(
    db: Session,
    workspace_data: WorkspaceCreate,
    user_id: int
):
    return create_workspace(
        db=db,
        name=workspace_data.name.strip(),
        owner_id=user_id
    )


def list_user_workspaces(
    db: Session,
    user_id: int
):
    return get_user_workspaces(
        db=db,
        user_id=user_id
    )