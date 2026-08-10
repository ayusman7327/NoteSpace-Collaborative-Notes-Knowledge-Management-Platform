from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.ai import (
    AIRequest,
    AIResponse,
    WorkspaceAIRequest,
)
from app.services.ai_service import generate_response
from app.services.auth_service import get_current_user
from app.services.page_service import check_workspace_membership
from app.services.workspace_ai_service import ask_workspace_ai


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/generate",
    response_model=AIResponse,
)
def generate(
    data: AIRequest,
    current_user: User = Depends(get_current_user),
):
    result = generate_response(
        data.prompt
    )

    return {
        "response": result
    }


@router.post(
    "/workspace/{workspace_id}",
    response_model=AIResponse,
)
def workspace_ai(
    workspace_id: int,
    data: WorkspaceAIRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )

    result = ask_workspace_ai(
        db=db,
        workspace_id=workspace_id,
        question=data.question,
    )

    return {
        "response": result
    }