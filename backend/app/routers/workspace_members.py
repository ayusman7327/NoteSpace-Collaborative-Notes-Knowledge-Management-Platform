from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.workspace_member import (
    WorkspaceMemberResponse,
    WorkspaceMemberRoleUpdate,
)
from app.services.workspace_member_service import (
    change_member_role,
    leave_workspace,
    list_members,
    remove_member,
)


router = APIRouter(
    prefix="/workspace-members",
    tags=["Workspace Members"],
)


@router.get(
    "/workspace/{workspace_id}",
    response_model=list[WorkspaceMemberResponse],
)
def get_workspace_members_route(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_members(
        db=db,
        workspace_id=workspace_id,
        current_user_id=current_user.id,
    )


@router.patch(
    "/workspace/{workspace_id}/member/{member_id}",
    response_model=WorkspaceMemberResponse,
)
def change_workspace_member_role_route(
    workspace_id: int,
    member_id: int,
    data: WorkspaceMemberRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return change_member_role(
        db=db,
        workspace_id=workspace_id,
        member_id=member_id,
        current_user_id=current_user.id,
        role=data.role,
    )


@router.delete(
    "/workspace/{workspace_id}/member/{member_id}",
)
def remove_workspace_member_route(
    workspace_id: int,
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return remove_member(
        db=db,
        workspace_id=workspace_id,
        member_id=member_id,
        current_user_id=current_user.id,
    )


@router.post(
    "/workspace/{workspace_id}/leave",
)
def leave_workspace_route(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return leave_workspace(
        db=db,
        workspace_id=workspace_id,
        current_user_id=current_user.id,
    )