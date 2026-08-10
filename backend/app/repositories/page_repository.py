from datetime import datetime, timezone

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.page import Page


def create_page(
    db: Session,
    workspace_id: int,
    parent_page_id: int | None,
    title: str,
    content: str,
    created_by: int,
) -> Page:
    page = Page(
        workspace_id=workspace_id,
        parent_page_id=parent_page_id,
        title=title,
        content=content,
        created_by=created_by,
    )

    db.add(page)
    db.commit()
    db.refresh(page)

    return page


def get_page_by_id(
    db: Session,
    page_id: int,
) -> Page | None:
    return (
        db.query(Page)
        .filter(
            Page.id == page_id,
            Page.is_deleted.is_(False),
        )
        .first()
    )


def get_page_by_id_including_deleted(
    db: Session,
    page_id: int,
) -> Page | None:
    return (
        db.query(Page)
        .filter(
            Page.id == page_id,
        )
        .first()
    )


def get_workspace_pages(
    db: Session,
    workspace_id: int,
) -> list[Page]:
    return (
        db.query(Page)
        .filter(
            Page.workspace_id == workspace_id,
            Page.is_deleted.is_(False),
        )
        .order_by(Page.created_at.asc())
        .all()
    )


def get_child_pages(
    db: Session,
    workspace_id: int,
    parent_page_id: int,
) -> list[Page]:
    return (
        db.query(Page)
        .filter(
            Page.workspace_id == workspace_id,
            Page.parent_page_id == parent_page_id,
            Page.is_deleted.is_(False),
        )
        .order_by(Page.created_at.asc())
        .all()
    )


def update_page(
    db: Session,
    page: Page,
    title: str | None,
    content: str | None,
) -> Page:
    if title is not None:
        page.title = title

    if content is not None:
        page.content = content

    db.commit()
    db.refresh(page)

    return page


def soft_delete_page(
    db: Session,
    page: Page,
) -> Page:
    page.is_deleted = True
    page.deleted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(page)

    return page


def restore_page(
    db: Session,
    page: Page,
) -> Page:
    page.is_deleted = False
    page.deleted_at = None

    db.commit()
    db.refresh(page)

    return page


def get_deleted_pages(
    db: Session,
    workspace_id: int,
) -> list[Page]:
    return (
        db.query(Page)
        .filter(
            Page.workspace_id == workspace_id,
            Page.is_deleted.is_(True),
        )
        .order_by(Page.deleted_at.desc())
        .all()
    )


def search_pages(
    db: Session,
    workspace_id: int,
    query: str,
) -> list[Page]:
    search_term = f"%{query}%"

    return (
        db.query(Page)
        .filter(
            Page.workspace_id == workspace_id,
            Page.is_deleted.is_(False),
            or_(
                Page.title.ilike(search_term),
                Page.content.ilike(search_term),
            ),
        )
        .order_by(Page.updated_at.desc())
        .all()
    )


def favorite_page(
    db: Session,
    page: Page,
) -> Page:
    page.is_favorite = True

    db.commit()
    db.refresh(page)

    return page


def unfavorite_page(
    db: Session,
    page: Page,
) -> Page:
    page.is_favorite = False

    db.commit()
    db.refresh(page)

    return page


def get_favorite_pages(
    db: Session,
    workspace_id: int,
) -> list[Page]:
    return (
        db.query(Page)
        .filter(
            Page.workspace_id == workspace_id,
            Page.is_deleted.is_(False),
            Page.is_favorite.is_(True),
        )
        .order_by(Page.updated_at.desc())
        .all()
    )


def update_last_opened(
    db: Session,
    page: Page,
) -> Page:
    page.last_opened_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(page)

    return page


def get_recent_pages(
    db: Session,
    workspace_id: int,
) -> list[Page]:
    return (
        db.query(Page)
        .filter(
            Page.workspace_id == workspace_id,
            Page.is_deleted.is_(False),
            Page.last_opened_at.is_not(None),
        )
        .order_by(Page.last_opened_at.desc())
        .limit(10)
        .all()
    )