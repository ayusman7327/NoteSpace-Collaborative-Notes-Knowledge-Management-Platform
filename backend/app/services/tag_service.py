from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.page_repository import get_page_by_id
from app.repositories.tag_repository import (
    attach_tag_to_page,
    create_tag,
    get_pages_by_tag,
    get_tag_by_id,
    get_tag_by_name,
    get_workspace_tags,
    remove_tag_from_page
)
from app.schemas.tag import TagCreate
from app.services.page_service import (
    check_edit_permission,
    check_workspace_membership
)


def create_workspace_tag(
    db: Session,
    workspace_id: int,
    tag_data: TagCreate,
    user_id: int
):
    membership = check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id
    )

    check_edit_permission(membership)

    tag_name = tag_data.name.strip().lower()

    existing_tag = get_tag_by_name(
        db=db,
        workspace_id=workspace_id,
        name=tag_name
    )

    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag already exists in this workspace"
        )

    try:
        return create_tag(
            db=db,
            workspace_id=workspace_id,
            name=tag_name
        )
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag already exists in this workspace"
        )


def list_workspace_tags(
    db: Session,
    workspace_id: int,
    user_id: int
):
    check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id
    )

    return get_workspace_tags(
        db=db,
        workspace_id=workspace_id
    )


def add_tag_to_page(
    db: Session,
    page_id: int,
    tag_id: int,
    user_id: int
):
    page = get_page_by_id(
        db=db,
        page_id=page_id
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )

    membership = check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id
    )

    check_edit_permission(membership)

    tag = get_tag_by_id(
        db=db,
        tag_id=tag_id
    )

    if tag is None or tag.workspace_id != page.workspace_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found in this workspace"
        )

    attach_tag_to_page(
        db=db,
        page=page,
        tag=tag
    )

    return tag


def delete_tag_from_page(
    db: Session,
    page_id: int,
    tag_id: int,
    user_id: int
):
    page = get_page_by_id(
        db=db,
        page_id=page_id
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )

    membership = check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id
    )

    check_edit_permission(membership)

    tag = get_tag_by_id(
        db=db,
        tag_id=tag_id
    )

    if tag is None or tag.workspace_id != page.workspace_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found in this workspace"
        )

    remove_tag_from_page(
        db=db,
        page=page,
        tag=tag
    )

    return tag


def list_pages_for_tag(
    db: Session,
    workspace_id: int,
    tag_id: int,
    user_id: int
):
    check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id
    )

    tag = get_tag_by_id(
        db=db,
        tag_id=tag_id
    )

    if tag is None or tag.workspace_id != workspace_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found in this workspace"
        )

    return get_pages_by_tag(
        db=db,
        workspace_id=workspace_id,
        tag_id=tag_id
    )