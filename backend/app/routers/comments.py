from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.comment import (
    CommentCreate,
    CommentResponse,
    CommentUpdate,
)
from app.services.comment_service import (
    create_page_comment,
    edit_comment,
    list_page_comments,
    mark_comment_open,
    mark_comment_resolved,
    remove_comment,
)


router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


@router.post(
    "/page/{page_id}",
    response_model=CommentResponse,
)
def create_comment(
    page_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_page_comment(
        db=db,
        page_id=page_id,
        user_id=current_user.id,
        comment_data=comment_data,
    )


@router.get(
    "/page/{page_id}",
    response_model=list[CommentResponse],
)
def get_comments(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_page_comments(
        db=db,
        page_id=page_id,
        user_id=current_user.id,
    )


@router.patch(
    "/{comment_id}",
    response_model=CommentResponse,
)
def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return edit_comment(
        db=db,
        comment_id=comment_id,
        user_id=current_user.id,
        comment_data=comment_data,
    )


@router.post(
    "/{comment_id}/resolve",
    response_model=CommentResponse,
)
def resolve_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return mark_comment_resolved(
        db=db,
        comment_id=comment_id,
        user_id=current_user.id,
    )


@router.post(
    "/{comment_id}/reopen",
    response_model=CommentResponse,
)
def reopen_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return mark_comment_open(
        db=db,
        comment_id=comment_id,
        user_id=current_user.id,
    )


@router.delete(
    "/{comment_id}",
)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return remove_comment(
        db=db,
        comment_id=comment_id,
        user_id=current_user.id,
    )