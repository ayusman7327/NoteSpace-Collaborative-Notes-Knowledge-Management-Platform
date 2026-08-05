from sqlalchemy.orm import Session

from app.repositories.activity_log_repository import (
    get_workspace_activity_logs
)
from app.services.page_service import check_workspace_membership


def list_workspace_activity(
    db: Session,
    workspace_id: int,
    user_id: int
):
    check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id
    )

    return get_workspace_activity_logs(
        db=db,
        workspace_id=workspace_id
    )