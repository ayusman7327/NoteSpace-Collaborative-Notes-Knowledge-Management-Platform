from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog
from app.models.workspace_member import WorkspaceMember


def check_activity_workspace_access(
    db: Session,
    workspace_id: int,
    user_id: int,
):
    membership = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        )
        .first()
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this workspace",
        )

    return membership


def create_activity_log(
    db: Session,
    workspace_id: int,
    user_id: int,
    action: str,
    entity_type: str | None = None,
    entity_id: int | None = None,
    description: str | None = None,
):
    activity = ActivityLog(
        workspace_id=workspace_id,
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


def list_workspace_activity_logs(
    db: Session,
    workspace_id: int,
    user_id: int,
    limit: int = 50,
):
    check_activity_workspace_access(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    return (
        db.query(ActivityLog)
        .filter(
            ActivityLog.workspace_id == workspace_id
        )
        .order_by(
            ActivityLog.created_at.desc()
        )
        .limit(limit)
        .all()
    )


def list_user_activity_logs(
    db: Session,
    user_id: int,
    limit: int = 50,
):
    return (
        db.query(ActivityLog)
        .filter(
            ActivityLog.user_id == user_id
        )
        .order_by(
            ActivityLog.created_at.desc()
        )
        .limit(limit)
        .all()
    )