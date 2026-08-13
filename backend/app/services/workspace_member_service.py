from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.workspace import Workspace
from app.repositories.workspace_member_repository import (
    get_workspace_member,
    get_workspace_member_by_id,
    get_workspace_members,
    remove_workspace_member,
    update_workspace_member_role,
)


ALLOWED_MEMBER_ROLES = {"editor", "viewer"}


def list_members(
    db: Session,
    workspace_id: int,
    current_user_id: int,
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

    membership = get_workspace_member(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user_id,
    )

    if (
        workspace.owner_id != current_user_id
        and membership is None
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this workspace",
        )

    return get_workspace_members(
        db=db,
        workspace_id=workspace_id,
    )


def change_member_role(
    db: Session,
    workspace_id: int,
    member_id: int,
    current_user_id: int,
    role: str,
):
    role = role.lower().strip()

    if role not in ALLOWED_MEMBER_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be editor or viewer",
        )

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

    if workspace.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the workspace owner can change member roles",
        )

    member = get_workspace_member_by_id(
        db=db,
        member_id=member_id,
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace member not found",
        )

    if member.workspace_id != workspace_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Member does not belong to this workspace",
        )

    if member.user_id == workspace.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The workspace owner role cannot be changed",
        )

    return update_workspace_member_role(
        db=db,
        member=member,
        role=role,
    )


def remove_member(
    db: Session,
    workspace_id: int,
    member_id: int,
    current_user_id: int,
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

    if workspace.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the workspace owner can remove members",
        )

    member = get_workspace_member_by_id(
        db=db,
        member_id=member_id,
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace member not found",
        )

    if member.workspace_id != workspace_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Member does not belong to this workspace",
        )

    if member.user_id == workspace.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The workspace owner cannot be removed",
        )

    remove_workspace_member(
        db=db,
        member=member,
    )

    return {
        "message": "Workspace member removed successfully"
    }


def leave_workspace(
    db: Session,
    workspace_id: int,
    current_user_id: int,
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

    if workspace.owner_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The owner cannot leave the workspace",
        )

    membership = get_workspace_member(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user_id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not a member of this workspace",
        )

    remove_workspace_member(
        db=db,
        member=membership,
    )

    return {
        "message": "You left the workspace successfully"
    }