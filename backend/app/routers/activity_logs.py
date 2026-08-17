from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.services.activity_log_service import (
    list_user_activity_logs,
    list_workspace_activity_logs,
)

router = APIRouter(
    prefix="/activity-logs",
    tags=["Activity Logs"],
)


@router.get("/workspace/{workspace_id}")
def get_workspace_activity_logs(
    workspace_id: int,
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_workspace_activity_logs(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
        limit=limit,
    )


@router.get("/me")
def get_my_activity_logs(
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_user_activity_logs(
        db=db,
        user_id=current_user.id,
        limit=limit,
    )