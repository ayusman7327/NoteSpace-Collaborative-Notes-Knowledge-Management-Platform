from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.page import PageResponse
from app.schemas.tag import TagCreate, TagResponse
from app.services.tag_service import (
    add_tag_to_page,
    create_workspace_tag,
    delete_tag_from_page,
    list_pages_for_tag,
    list_workspace_tags
)


router = APIRouter(
    prefix="/workspaces",
    tags=["Tags"]
)


@router.post(
    "/{workspace_id}/tags",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED
)
def create_tag(
    workspace_id: int,
    tag_data: TagCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_workspace_tag(
        db=db,
        workspace_id=workspace_id,
        tag_data=tag_data,
        user_id=current_user.id
    )


@router.get(
    "/{workspace_id}/tags",
    response_model=list[TagResponse]
)
def get_tags(
    workspace_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return list_workspace_tags(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id
    )


@router.post(
    "/{workspace_id}/pages/{page_id}/tags/{tag_id}",
    response_model=TagResponse
)
def attach_tag(
    workspace_id: int,
    page_id: int,
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return add_tag_to_page(
        db=db,
        page_id=page_id,
        tag_id=tag_id,
        user_id=current_user.id
    )


@router.delete(
    "/{workspace_id}/pages/{page_id}/tags/{tag_id}",
    response_model=TagResponse
)
def remove_tag(
    workspace_id: int,
    page_id: int,
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_tag_from_page(
        db=db,
        page_id=page_id,
        tag_id=tag_id,
        user_id=current_user.id
    )


@router.get(
    "/{workspace_id}/tags/{tag_id}/pages",
    response_model=list[PageResponse]
)
def get_pages_by_tag(
    workspace_id: int,
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return list_pages_for_tag(
        db=db,
        workspace_id=workspace_id,
        tag_id=tag_id,
        user_id=current_user.id
    )