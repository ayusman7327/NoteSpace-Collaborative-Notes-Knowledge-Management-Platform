from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.page import Page
from app.models.page_version import PageVersion
from app.models.workspace import WorkspaceRole
from app.models.workspace_member import WorkspaceMember
from app.schemas.page import PageCreate, PageUpdate


def check_workspace_membership(
    db: Session,
    workspace_id: int,
    user_id: int,
):
    membership = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        )
        .first()
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this workspace",
        )

    return membership


def check_edit_permission(membership):
    role = membership.role

    if hasattr(role, "value"):
        role = role.value

    allowed_roles = {
        WorkspaceRole.OWNER.value,
        WorkspaceRole.EDITOR.value,
        "owner",
        "editor",
    }

    if role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to edit this workspace",
        )


def create_new_page(
    db: Session,
    workspace_id: int,
    user_id: int,
    page_data: PageCreate,
):
    membership = check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    check_edit_permission(membership)

    parent_page_id = getattr(
        page_data,
        "parent_page_id",
        None,
    )

    if parent_page_id is not None:
        parent_page = (
            db.query(Page)
            .filter(
                Page.id == parent_page_id,
                Page.workspace_id == workspace_id,
                Page.is_deleted.is_(False),
            )
            .first()
        )

        if parent_page is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent page not found",
            )

    title = getattr(
        page_data,
        "title",
        "Untitled",
    )

    content = getattr(
        page_data,
        "content",
        "",
    )

    page = Page(
        workspace_id=workspace_id,
        parent_page_id=parent_page_id,
        title=title or "Untitled",
        content=content or "",
        created_by=user_id,
    )

    db.add(page)
    db.commit()
    db.refresh(page)

    return page


def list_workspace_pages(
    db: Session,
    workspace_id: int,
    user_id: int,
):
    check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    return (
        db.query(Page)
        .filter(
            Page.workspace_id == workspace_id,
            Page.is_deleted.is_(False),
        )
        .order_by(
            Page.created_at.asc()
        )
        .all()
    )


def get_page_details(
    db: Session,
    page_id: int,
    user_id: int,
):
    page = (
        db.query(Page)
        .filter(
            Page.id == page_id,
            Page.is_deleted.is_(False),
        )
        .first()
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

    return page


def open_page(
    db: Session,
    page_id: int,
    user_id: int,
):
    page = get_page_details(
        db=db,
        page_id=page_id,
        user_id=user_id,
    )

    page.last_opened_at = datetime.utcnow()

    db.commit()
    db.refresh(page)

    return page


def list_recent_pages(
    db: Session,
    workspace_id: int,
    user_id: int,
):
    check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    return (
        db.query(Page)
        .filter(
            Page.workspace_id == workspace_id,
            Page.is_deleted.is_(False),
            Page.last_opened_at.isnot(None),
        )
        .order_by(
            Page.last_opened_at.desc()
        )
        .limit(20)
        .all()
    )


def list_child_pages(
    db: Session,
    page_id: int,
    user_id: int,
):
    parent_page = get_page_details(
        db=db,
        page_id=page_id,
        user_id=user_id,
    )

    return (
        db.query(Page)
        .filter(
            Page.workspace_id == parent_page.workspace_id,
            Page.parent_page_id == page_id,
            Page.is_deleted.is_(False),
        )
        .order_by(
            Page.created_at.asc()
        )
        .all()
    )


def _create_page_version(
    db: Session,
    page: Page,
    user_id: int,
):
    try:
        version = PageVersion(
            page_id=page.id,
            title=page.title,
            content=page.content,
            created_by=user_id,
        )

        db.add(version)

    except TypeError:
        pass


def update_existing_page(
    db: Session,
    page_id: int,
    user_id: int,
    page_data: PageUpdate,
):
    page = get_page_details(
        db=db,
        page_id=page_id,
        user_id=user_id,
    )

    membership = check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id,
    )

    check_edit_permission(membership)

    _create_page_version(
        db=db,
        page=page,
        user_id=user_id,
    )

    update_data = page_data.model_dump(
        exclude_unset=True
    )

    if "title" in update_data:
        page.title = (
            update_data["title"].strip()
            or "Untitled"
        )

    if "content" in update_data:
        page.content = (
            update_data["content"]
            or ""
        )

    if "parent_page_id" in update_data:
        parent_page_id = update_data[
            "parent_page_id"
        ]

        if parent_page_id == page.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A page cannot be its own parent",
            )

        if parent_page_id is not None:
            parent_page = (
                db.query(Page)
                .filter(
                    Page.id == parent_page_id,
                    Page.workspace_id
                    == page.workspace_id,
                    Page.is_deleted.is_(False),
                )
                .first()
            )

            if parent_page is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent page not found",
                )

        page.parent_page_id = parent_page_id

    page.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(page)

    return page


def list_page_versions(
    db: Session,
    page_id: int,
    user_id: int,
):
    page = get_page_details(
        db=db,
        page_id=page_id,
        user_id=user_id,
    )

    check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id,
    )

    return (
        db.query(PageVersion)
        .filter(
            PageVersion.page_id == page_id
        )
        .order_by(
            PageVersion.created_at.desc()
        )
        .all()
    )


def restore_page_version(
    db: Session,
    page_id: int,
    version_id: int,
    user_id: int,
):
    page = get_page_details(
        db=db,
        page_id=page_id,
        user_id=user_id,
    )

    membership = check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id,
    )

    check_edit_permission(membership)

    version = (
        db.query(PageVersion)
        .filter(
            PageVersion.id == version_id,
            PageVersion.page_id == page_id,
        )
        .first()
    )

    if version is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page version not found",
        )

    _create_page_version(
        db=db,
        page=page,
        user_id=user_id,
    )

    page.title = version.title
    page.content = version.content
    page.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(page)

    return page


def delete_page(
    db: Session,
    page_id: int,
    user_id: int,
):
    page = get_page_details(
        db=db,
        page_id=page_id,
        user_id=user_id,
    )

    membership = check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id,
    )

    check_edit_permission(membership)

    page.is_deleted = True
    page.deleted_at = datetime.utcnow()

    db.commit()
    db.refresh(page)

    return page


def restore_deleted_page(
    db: Session,
    page_id: int,
    user_id: int,
):
    page = (
        db.query(Page)
        .filter(
            Page.id == page_id,
            Page.is_deleted.is_(True),
        )
        .first()
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deleted page not found",
        )

    membership = check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id,
    )

    check_edit_permission(membership)

    page.is_deleted = False
    page.deleted_at = None

    db.commit()
    db.refresh(page)

    return page


def list_deleted_pages(
    db: Session,
    workspace_id: int,
    user_id: int,
):
    check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    return (
        db.query(Page)
        .filter(
            Page.workspace_id == workspace_id,
            Page.is_deleted.is_(True),
        )
        .order_by(
            Page.deleted_at.desc()
        )
        .all()
    )


def search_workspace_pages(
    db: Session,
    workspace_id: int,
    user_id: int,
    query: str,
):
    check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    cleaned_query = query.strip()

    if not cleaned_query:
        return []

    pattern = f"%{cleaned_query}%"

    return (
        db.query(Page)
        .filter(
            Page.workspace_id == workspace_id,
            Page.is_deleted.is_(False),
            or_(
                Page.title.ilike(pattern),
                Page.content.ilike(pattern),
            ),
        )
        .order_by(
            Page.updated_at.desc()
        )
        .all()
    )


def mark_page_favorite(
    db: Session,
    page_id: int,
    user_id: int,
):
    page = get_page_details(
        db=db,
        page_id=page_id,
        user_id=user_id,
    )

    page.is_favorite = True

    db.commit()
    db.refresh(page)

    return page


def remove_page_favorite(
    db: Session,
    page_id: int,
    user_id: int,
):
    page = get_page_details(
        db=db,
        page_id=page_id,
        user_id=user_id,
    )

    page.is_favorite = False

    db.commit()
    db.refresh(page)

    return page


def list_favorite_pages(
    db: Session,
    workspace_id: int,
    user_id: int,
):
    check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    return (
        db.query(Page)
        .filter(
            Page.workspace_id == workspace_id,
            Page.is_deleted.is_(False),
            Page.is_favorite.is_(True),
        )
        .order_by(
            Page.updated_at.desc()
        )
        .all()
    )