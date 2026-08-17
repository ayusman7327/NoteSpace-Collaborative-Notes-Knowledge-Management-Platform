from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.workspace_invitation import (
    WorkspaceInvitationCreate,
    WorkspaceInvitationResponse,
)
from app.services.workspace_invitation_service import (
    accept_workspace_invitation,
    cancel_workspace_invitation,
    invite_user_to_workspace,
    list_my_pending_invitations,
    list_workspace_invitations,
    reject_workspace_invitation,
)


router = APIRouter(
    prefix="/workspace-invitations",
    tags=["Workspace Invitations"],
)


@router.post(
    "/workspace/{workspace_id}",
    response_model=WorkspaceInvitationResponse,
)
def create_invitation(
    workspace_id: int,
    data: WorkspaceInvitationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return invite_user_to_workspace(
        db=db,
        workspace_id=workspace_id,
        invited_by=current_user.id,
        email=data.email,
        role=data.role,
    )


@router.get(
    "/workspace/{workspace_id}",
    response_model=list[WorkspaceInvitationResponse],
)
def get_workspace_invitations_route(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_workspace_invitations(
        db=db,
        workspace_id=workspace_id,
        current_user_id=current_user.id,
    )


@router.get(
    "/my",
    response_model=list[WorkspaceInvitationResponse],
)
def get_my_invitations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_my_pending_invitations(
        db=db,
        current_user=current_user,
    )


@router.post(
    "/{invitation_id}/accept",
    response_model=WorkspaceInvitationResponse,
)
def accept_invitation_route(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return accept_workspace_invitation(
        db=db,
        invitation_id=invitation_id,
        current_user=current_user,
    )


@router.post(
    "/{invitation_id}/reject",
    response_model=WorkspaceInvitationResponse,
)
def reject_invitation_route(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return reject_workspace_invitation(
        db=db,
        invitation_id=invitation_id,
        current_user=current_user,
    )


@router.post(
    "/{invitation_id}/cancel",
    response_model=WorkspaceInvitationResponse,
)
def cancel_invitation_route(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cancel_workspace_invitation(
        db=db,
        invitation_id=invitation_id,
        current_user_id=current_user.id,
    )