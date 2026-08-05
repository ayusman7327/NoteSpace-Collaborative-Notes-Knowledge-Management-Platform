from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog


def create_activity_log(
    db: Session,
    workspace_id: int,
    user_id: int,
    action: str,
    page_id: int | None = None
) -> ActivityLog:
    activity = ActivityLog(
        workspace_id=workspace_id,
        page_id=page_id,
        user_id=user_id,
        action=action
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


def get_workspace_activity_logs(
    db: Session,
    workspace_id: int
) -> list[ActivityLog]:
    return (
        db.query(ActivityLog)
        .filter(
            ActivityLog.workspace_id == workspace_id
        )
        .order_by(ActivityLog.created_at.desc())
        .all()
    )