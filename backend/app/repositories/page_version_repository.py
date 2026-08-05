from sqlalchemy.orm import Session

from app.models.page_version import PageVersion


def create_page_version(
    db: Session,
    page_id: int,
    content_snapshot: str,
    edited_by: int
) -> PageVersion:
    version = PageVersion(
        page_id=page_id,
        content_snapshot=content_snapshot,
        edited_by=edited_by
    )

    db.add(version)
    db.commit()
    db.refresh(version)

    return version


def get_page_versions(
    db: Session,
    page_id: int
) -> list[PageVersion]:
    return (
        db.query(PageVersion)
        .filter(PageVersion.page_id == page_id)
        .order_by(PageVersion.created_at.desc())
        .all()
    )


def get_page_version_by_id(
    db: Session,
    version_id: int
) -> PageVersion | None:
    return (
        db.query(PageVersion)
        .filter(PageVersion.id == version_id)
        .first()
    )