from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.workspace import Workspace, WorkspaceRole
from app.models.workspace_member import WorkspaceMember
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate


def get_workspace_membership(
    db: Session,
    workspace_id: int,
    user_id: int,
):
    return (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        )
        .first()
    )


def require_workspace_membership(
    db: Session,
    workspace_id: int,
    user_id: int,
):
    membership = get_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this workspace",
        )

    return membership


def require_workspace_owner(
    db: Session,
    workspace_id: int,
    user_id: int,
):
    workspace = (
        db.query(Workspace)
        .filter(
            Workspace.id == workspace_id
        )
        .first()
    )

    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    if workspace.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the workspace owner can perform this action",
        )

    return workspace


def create_workspace(
    db: Session,
    user_id: int,
    workspace_data: WorkspaceCreate,
):
    workspace = Workspace(
        name=workspace_data.name.strip(),
        description=(
            workspace_data.description.strip()
            if workspace_data.description
            else None
        ),
        owner_id=user_id,
    )

    db.add(workspace)
    db.flush()

    owner_membership = WorkspaceMember(
        workspace_id=workspace.id,
        user_id=user_id,
        role=WorkspaceRole.OWNER.value,
    )

    db.add(owner_membership)

    db.commit()
    db.refresh(workspace)

    return workspace


def get_user_workspaces(
    db: Session,
    user_id: int,
):
    memberships = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.user_id == user_id
        )
        .all()
    )

    workspace_ids = [
        membership.workspace_id
        for membership in memberships
    ]

    if not workspace_ids:
        return []

    return (
        db.query(Workspace)
        .filter(
            Workspace.id.in_(workspace_ids)
        )
        .order_by(
            Workspace.updated_at.desc()
        )
        .all()
    )


def get_workspace(
    db: Session,
    workspace_id: int,
    user_id: int,
):
    workspace = (
        db.query(Workspace)
        .filter(
            Workspace.id == workspace_id
        )
        .first()
    )

    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    require_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    return workspace


def update_workspace(
    db: Session,
    workspace_id: int,
    user_id: int,
    workspace_data: WorkspaceUpdate,
):
    workspace = require_workspace_owner(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    update_data = workspace_data.model_dump(
        exclude_unset=True
    )

    if "name" in update_data:
        new_name = update_data["name"]

        if new_name is not None:
            new_name = new_name.strip()

            if not new_name:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Workspace name cannot be empty",
                )

            workspace.name = new_name

    if "description" in update_data:
        description = update_data["description"]

        workspace.description = (
            description.strip()
            if description
            else None
        )

    db.commit()
    db.refresh(workspace)

    return workspace


def delete_workspace(
    db: Session,
    workspace_id: int,
    user_id: int,
):
    workspace = require_workspace_owner(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    db.delete(workspace)
    db.commit()

    return {
        "message": "Workspace deleted successfully"
    }