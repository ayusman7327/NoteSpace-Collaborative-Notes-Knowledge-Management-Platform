from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.activity_log import ActivityLogResponse
from app.services.activity_log_service import (
    list_workspace_activity
)


router = APIRouter(
    prefix="/workspaces",
    tags=["Activity Logs"]
)


@router.get(
    "/{workspace_id}/activity",
    response_model=list[ActivityLogResponse]
)
def get_workspace_activity(
    workspace_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return list_workspace_activity(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id
    )