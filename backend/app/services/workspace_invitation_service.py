from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.workspace import Workspace
from app.repositories.workspace_invitation_repository import (
    accept_invitation,
    cancel_invitation,
    create_invitation,
    get_invitation_by_id,
    get_pending_invitation,
    get_user_pending_invitations,
    get_workspace_invitations,
    reject_invitation,
)
from app.repositories.workspace_member_repository import (
    create_workspace_member,
    get_workspace_member,
)


ALLOWED_ROLES = {
    "editor",
    "viewer",
}


def invite_user_to_workspace(
    db: Session,
    workspace_id: int,
    invited_by: int,
    email: str,
    role: str,
):
    email = email.lower().strip()
    role = role.lower().strip()

    if role not in ALLOWED_ROLES:
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

    if workspace.owner_id != invited_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the workspace owner can invite members",
        )

    inviter = (
        db.query(User)
        .filter(
            User.id == invited_by
        )
        .first()
    )

    if inviter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inviting user not found",
        )

    if inviter.email.lower() == email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot invite yourself",
        )

    invited_user = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )

    if invited_user is not None:
        existing_member = get_workspace_member(
            db=db,
            workspace_id=workspace_id,
            user_id=invited_user.id,
        )

        if existing_member is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This user is already a workspace member",
            )

    existing_invitation = get_pending_invitation(
        db=db,
        workspace_id=workspace_id,
        email=email,
    )

    if existing_invitation is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A pending invitation already exists for this email",
        )

    return create_invitation(
        db=db,
        workspace_id=workspace_id,
        invited_by=invited_by,
        email=email,
        role=role,
    )


def list_workspace_invitations(
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

    if workspace.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the workspace owner can view invitations",
        )

    return get_workspace_invitations(
        db=db,
        workspace_id=workspace_id,
    )


def list_my_pending_invitations(
    db: Session,
    current_user: User,
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    return get_user_pending_invitations(
        db=db,
        email=current_user.email,
    )


def accept_workspace_invitation(
    db: Session,
    invitation_id: int,
    current_user: User,
):
    invitation = get_invitation_by_id(
        db=db,
        invitation_id=invitation_id,
    )

    if invitation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    if invitation.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation is no longer pending",
        )

    if (
        invitation.email.lower()
        != current_user.email.lower()
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This invitation does not belong to you",
        )

    existing_member = get_workspace_member(
        db=db,
        workspace_id=invitation.workspace_id,
        user_id=current_user.id,
    )

    if existing_member is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already a member of this workspace",
        )

    create_workspace_member(
        db=db,
        workspace_id=invitation.workspace_id,
        user_id=current_user.id,
        role=invitation.role,
    )

    return accept_invitation(
        db=db,
        invitation=invitation,
    )


def reject_workspace_invitation(
    db: Session,
    invitation_id: int,
    current_user: User,
):
    invitation = get_invitation_by_id(
        db=db,
        invitation_id=invitation_id,
    )

    if invitation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    if invitation.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation is no longer pending",
        )

    if (
        invitation.email.lower()
        != current_user.email.lower()
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This invitation does not belong to you",
        )

    return reject_invitation(
        db=db,
        invitation=invitation,
    )


def cancel_workspace_invitation(
    db: Session,
    invitation_id: int,
    current_user_id: int,
):
    invitation = get_invitation_by_id(
        db=db,
        invitation_id=invitation_id,
    )

    if invitation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    workspace = (
        db.query(Workspace)
        .filter(
            Workspace.id
            == invitation.workspace_id
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
            detail="Only the workspace owner can cancel invitations",
        )

    if invitation.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending invitations can be cancelled",
        )

    return cancel_invitation(
        db=db,
        invitation=invitation,
    )