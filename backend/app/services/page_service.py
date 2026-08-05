from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.workspace import WorkspaceMember, WorkspaceRole
from app.repositories.page_repository import (
    create_page,
    get_child_pages,
    get_page_by_id,
    get_workspace_pages,
    update_page
)
from app.repositories.page_version_repository import (
    create_page_version,
    get_page_version_by_id,
    get_page_versions
)
from app.schemas.page import PageCreate, PageUpdate


def check_workspace_membership(
    db: Session,
    workspace_id: int,
    user_id: int
) -> WorkspaceMember:
    membership = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id
        )
        .first()
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this workspace"
        )

    return membership


def check_edit_permission(
    membership: WorkspaceMember
) -> None:
    if membership.role not in [
        WorkspaceRole.OWNER,
        WorkspaceRole.EDITOR
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to edit pages"
        )


def create_new_page(
    db: Session,
    page_data: PageCreate,
    user_id: int
):
    membership = check_workspace_membership(
        db=db,
        workspace_id=page_data.workspace_id,
        user_id=user_id
    )

    check_edit_permission(membership)

    if page_data.parent_page_id is not None:
        parent_page = get_page_by_id(
            db=db,
            page_id=page_data.parent_page_id
        )

        if (
            parent_page is None
            or parent_page.workspace_id != page_data.workspace_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent page not found in this workspace"
            )

    return create_page(
        db=db,
        workspace_id=page_data.workspace_id,
        parent_page_id=page_data.parent_page_id,
        title=page_data.title.strip(),
        content=page_data.content,
        created_by=user_id
    )


def list_workspace_pages(
    db: Session,
    workspace_id: int,
    user_id: int
):
    check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id
    )

    return get_workspace_pages(
        db=db,
        workspace_id=workspace_id
    )


def get_page_details(
    db: Session,
    page_id: int,
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

    check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id
    )

    return page


def list_child_pages(
    db: Session,
    workspace_id: int,
    parent_page_id: int,
    user_id: int
):
    check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id
    )

    parent_page = get_page_by_id(
        db=db,
        page_id=parent_page_id
    )

    if (
        parent_page is None
        or parent_page.workspace_id != workspace_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent page not found"
        )

    return get_child_pages(
        db=db,
        workspace_id=workspace_id,
        parent_page_id=parent_page_id
    )


def update_existing_page(
    db: Session,
    page_id: int,
    page_data: PageUpdate,
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

    create_page_version(
        db=db,
        page_id=page.id,
        content_snapshot=page.content,
        edited_by=user_id
    )

    title = (
        page_data.title.strip()
        if page_data.title is not None
        else None
    )

    return update_page(
        db=db,
        page=page,
        title=title,
        content=page_data.content
    )


def list_page_versions(
    db: Session,
    page_id: int,
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

    check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id
    )

    return get_page_versions(
        db=db,
        page_id=page_id
    )


def restore_page_version(
    db: Session,
    page_id: int,
    version_id: int,
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

    version = get_page_version_by_id(
        db=db,
        version_id=version_id
    )

    if version is None or version.page_id != page.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page version not found"
        )

    create_page_version(
        db=db,
        page_id=page.id,
        content_snapshot=page.content,
        edited_by=user_id
    )

    return update_page(
        db=db,
        page=page,
        title=None,
        content=version.content_snapshot
    )