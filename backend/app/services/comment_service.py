from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.comment_repository import (
    create_comment,
    delete_comment,
    get_comment_by_id,
    get_page_comments,
    reopen_comment,
    resolve_comment,
    update_comment,
)
from app.repositories.page_repository import get_page_by_id
from app.schemas.comment import CommentCreate, CommentUpdate
from app.services.page_service import check_workspace_membership


def create_page_comment(
    db: Session,
    page_id: int,
    user_id: int,
    comment_data: CommentCreate,
):
    page = get_page_by_id(
        db=db,
        page_id=page_id,
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found",
        )

    check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id,
    )

    return create_comment(
        db=db,
        page_id=page_id,
        user_id=user_id,
        content=comment_data.content.strip(),
    )


def list_page_comments(
    db: Session,
    page_id: int,
    user_id: int,
):
    page = get_page_by_id(
        db=db,
        page_id=page_id,
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found",
        )

    check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id,
    )

    return get_page_comments(
        db=db,
        page_id=page_id,
    )


def edit_comment(
    db: Session,
    comment_id: int,
    user_id: int,
    comment_data: CommentUpdate,
):
    comment = get_comment_by_id(
        db=db,
        comment_id=comment_id,
    )

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    page = get_page_by_id(
        db=db,
        page_id=comment.page_id,
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found",
        )

    check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id,
    )

    if comment.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own comments",
        )

    return update_comment(
        db=db,
        comment=comment,
        content=comment_data.content.strip(),
    )


def remove_comment(
    db: Session,
    comment_id: int,
    user_id: int,
):
    comment = get_comment_by_id(
        db=db,
        comment_id=comment_id,
    )

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    page = get_page_by_id(
        db=db,
        page_id=comment.page_id,
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found",
        )

    check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id,
    )

    if comment.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own comments",
        )

    delete_comment(
        db=db,
        comment=comment,
    )

    return {
        "message": "Comment deleted successfully"
    }


def mark_comment_resolved(
    db: Session,
    comment_id: int,
    user_id: int,
):
    comment = get_comment_by_id(
        db=db,
        comment_id=comment_id,
    )

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    page = get_page_by_id(
        db=db,
        page_id=comment.page_id,
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found",
        )

    check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id,
    )

    return resolve_comment(
        db=db,
        comment=comment,
    )


def mark_comment_open(
    db: Session,
    comment_id: int,
    user_id: int,
):
    comment = get_comment_by_id(
        db=db,
        comment_id=comment_id,
    )

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    page = get_page_by_id(
        db=db,
        page_id=comment.page_id,
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found",
        )

    check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id,
    )

    return reopen_comment(
        db=db,
        comment=comment,
    )