from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.page import (
    PageCreate,
    PageResponse,
    PageUpdate,
)
from app.services.page_service import (
    create_new_page,
    delete_page,
    get_page_details,
    list_deleted_pages,
    list_favorite_pages,
    list_recent_pages,
    list_workspace_pages,
    mark_page_favorite,
    open_page,
    remove_page_favorite,
    restore_deleted_page,
    restore_page_version,
    search_workspace_pages,
    update_existing_page,
)


router = APIRouter(
    prefix="/pages",
    tags=["Pages"],
)


@router.post(
    "/workspace/{workspace_id}",
    response_model=PageResponse,
)
def create_page_route(
    workspace_id: int,
    data: PageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_new_page(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
        page_data=data,
    )


@router.get(
    "/workspace/{workspace_id}",
    response_model=list[PageResponse],
)
def get_workspace_pages_route(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_workspace_pages(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )


@router.get(
    "/{page_id}",
    response_model=PageResponse,
)
def get_page_route(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_page_details(
        db=db,
        page_id=page_id,
        user_id=current_user.id,
    )


@router.post(
    "/{page_id}/open",
    response_model=PageResponse,
)
def open_page_route(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return open_page(
        db=db,
        page_id=page_id,
        user_id=current_user.id,
    )


@router.patch(
    "/{page_id}",
    response_model=PageResponse,
)
def update_page_route(
    page_id: int,
    data: PageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_existing_page(
        db=db,
        page_id=page_id,
        user_id=current_user.id,
        page_data=data,
    )


@router.delete(
    "/{page_id}",
    response_model=PageResponse,
)
def delete_page_route(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_page(
        db=db,
        page_id=page_id,
        user_id=current_user.id,
    )


@router.post(
    "/{page_id}/restore",
    response_model=PageResponse,
)
def restore_page_route(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return restore_deleted_page(
        db=db,
        page_id=page_id,
        user_id=current_user.id,
    )


@router.post(
    "/{page_id}/favorite",
    response_model=PageResponse,
)
def favorite_page_route(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return mark_page_favorite(
        db=db,
        page_id=page_id,
        user_id=current_user.id,
    )


@router.delete(
    "/{page_id}/favorite",
    response_model=PageResponse,
)
def unfavorite_page_route(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return remove_page_favorite(
        db=db,
        page_id=page_id,
        user_id=current_user.id,
    )


@router.get(
    "/workspace/{workspace_id}/trash",
    response_model=list[PageResponse],
)
def get_trash_route(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_deleted_pages(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )


@router.get(
    "/workspace/{workspace_id}/recent",
    response_model=list[PageResponse],
)
def get_recent_pages_route(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_recent_pages(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )


@router.get(
    "/workspace/{workspace_id}/favorites",
    response_model=list[PageResponse],
)
def get_favorite_pages_route(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_favorite_pages(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )


@router.get(
    "/workspace/{workspace_id}/search",
    response_model=list[PageResponse],
)
def search_pages_route(
    workspace_id: int,
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return search_workspace_pages(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
        query=q,
    )


@router.post(
    "/{page_id}/versions/{version_id}/restore",
    response_model=PageResponse,
)
def restore_version_route(
    page_id: int,
    version_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return restore_page_version(
        db=db,
        page_id=page_id,
        version_id=version_id,
        user_id=current_user.id,
    )