from sqlalchemy.orm import Session

from app.models.page import Page


def create_page(
    db: Session,
    workspace_id: int,
    parent_page_id: int | None,
    title: str,
    content: str,
    created_by: int
) -> Page:
    page = Page(
        workspace_id=workspace_id,
        parent_page_id=parent_page_id,
        title=title,
        content=content,
        created_by=created_by
    )

    db.add(page)
    db.commit()
    db.refresh(page)

    return page


def get_page_by_id(
    db: Session,
    page_id: int
) -> Page | None:
    return (
        db.query(Page)
        .filter(
            Page.id == page_id,
            Page.is_deleted.is_(False)
        )
        .first()
    )


def get_workspace_pages(
    db: Session,
    workspace_id: int
) -> list[Page]:
    return (
        db.query(Page)
        .filter(
            Page.workspace_id == workspace_id,
            Page.is_deleted.is_(False)
        )
        .order_by(Page.created_at.asc())
        .all()
    )


def get_child_pages(
    db: Session,
    workspace_id: int,
    parent_page_id: int
) -> list[Page]:
    return (
        db.query(Page)
        .filter(
            Page.workspace_id == workspace_id,
            Page.parent_page_id == parent_page_id,
            Page.is_deleted.is_(False)
        )
        .order_by(Page.created_at.asc())
        .all()
    )


def update_page(
    db: Session,
    page: Page,
    title: str | None,
    content: str | None
) -> Page:
    if title is not None:
        page.title = title

    if content is not None:
        page.content = content

    db.commit()
    db.refresh(page)

    return page