from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.page import (
    PageCreate,
    PageResponse,
    PageUpdate
)
from app.schemas.page_version import PageVersionResponse
from app.services.page_service import (
    create_new_page,
    delete_page,
    get_page_details,
    list_child_pages,
    list_deleted_pages,
    list_page_versions,
    list_workspace_pages,
    restore_deleted_page,
    restore_page_version,
    search_workspace_pages,
    update_existing_page
)


router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)


@router.post(
    "",
    response_model=PageResponse,
    status_code=status.HTTP_201_CREATED
)
def create_page(
    page_data: PageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_new_page(
        db=db,
        page_data=page_data,
        user_id=current_user.id
    )


@router.get(
    "/workspace/{workspace_id}",
    response_model=list[PageResponse]
)
def get_workspace_pages(
    workspace_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return list_workspace_pages(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id
    )


@router.get(
    "/workspace/{workspace_id}/search",
    response_model=list[PageResponse]
)
def search_pages_route(
    workspace_id: int,
    q: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return search_workspace_pages(
        db=db,
        workspace_id=workspace_id,
        query=q,
        user_id=current_user.id
    )


@router.get(
    "/workspace/{workspace_id}/trash",
    response_model=list[PageResponse]
)
def get_deleted_pages_route(
    workspace_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return list_deleted_pages(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id
    )


@router.get(
    "/workspace/{workspace_id}/{parent_page_id}/children",
    response_model=list[PageResponse]
)
def get_children(
    workspace_id: int,
    parent_page_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return list_child_pages(
        db=db,
        workspace_id=workspace_id,
        parent_page_id=parent_page_id,
        user_id=current_user.id
    )


@router.get(
    "/{page_id}",
    response_model=PageResponse
)
def get_page(
    page_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_page_details(
        db=db,
        page_id=page_id,
        user_id=current_user.id
    )


@router.patch(
    "/{page_id}",
    response_model=PageResponse
)
def update_page(
    page_id: int,
    page_data: PageUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_existing_page(
        db=db,
        page_id=page_id,
        page_data=page_data,
        user_id=current_user.id
    )


@router.delete(
    "/{page_id}",
    response_model=PageResponse
)
def delete_page_route(
    page_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_page(
        db=db,
        page_id=page_id,
        user_id=current_user.id
    )


@router.post(
    "/{page_id}/restore",
    response_model=PageResponse
)
def restore_page_route(
    page_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return restore_deleted_page(
        db=db,
        page_id=page_id,
        user_id=current_user.id
    )


@router.get(
    "/{page_id}/versions",
    response_model=list[PageVersionResponse]
)
def get_versions(
    page_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return list_page_versions(
        db=db,
        page_id=page_id,
        user_id=current_user.id
    )


@router.post(
    "/{page_id}/versions/{version_id}/restore",
    response_model=PageResponse
)
def restore_version(
    page_id: int,
    version_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return restore_page_version(
        db=db,
        page_id=page_id,
        version_id=version_id,
        user_id=current_user.id
    )