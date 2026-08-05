from sqlalchemy.orm import Session

from app.models.page import Page
from app.models.tag import Tag


def create_tag(
    db: Session,
    workspace_id: int,
    name: str
) -> Tag:
    tag = Tag(
        workspace_id=workspace_id,
        name=name
    )

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag


def get_tag_by_id(
    db: Session,
    tag_id: int
) -> Tag | None:
    return (
        db.query(Tag)
        .filter(Tag.id == tag_id)
        .first()
    )


def get_tag_by_name(
    db: Session,
    workspace_id: int,
    name: str
) -> Tag | None:
    return (
        db.query(Tag)
        .filter(
            Tag.workspace_id == workspace_id,
            Tag.name == name
        )
        .first()
    )


def get_workspace_tags(
    db: Session,
    workspace_id: int
) -> list[Tag]:
    return (
        db.query(Tag)
        .filter(Tag.workspace_id == workspace_id)
        .order_by(Tag.name.asc())
        .all()
    )


def attach_tag_to_page(
    db: Session,
    page: Page,
    tag: Tag
) -> Page:
    if tag not in page.tags:
        page.tags.append(tag)
        db.commit()
        db.refresh(page)

    return page


def remove_tag_from_page(
    db: Session,
    page: Page,
    tag: Tag
) -> Page:
    if tag in page.tags:
        page.tags.remove(tag)
        db.commit()
        db.refresh(page)

    return page


def get_pages_by_tag(
    db: Session,
    workspace_id: int,
    tag_id: int
) -> list[Page]:
    return (
        db.query(Page)
        .join(Page.tags)
        .filter(
            Page.workspace_id == workspace_id,
            Tag.id == tag_id,
            Page.is_deleted.is_(False)
        )
        .order_by(Page.updated_at.desc())
        .all()
    )