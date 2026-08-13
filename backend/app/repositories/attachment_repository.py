from sqlalchemy.orm import Session

from app.models.attachment import Attachment


def create_attachment(
    db: Session,
    page_id: int,
    uploaded_by: int,
    file_name: str,
    stored_name: str,
    file_type: str | None,
    file_size: int,
    file_url: str,
) -> Attachment:
    attachment = Attachment(
        page_id=page_id,
        uploaded_by=uploaded_by,
        file_name=file_name,
        stored_name=stored_name,
        file_type=file_type,
        file_size=file_size,
        file_url=file_url,
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment


def get_attachment_by_id(
    db: Session,
    attachment_id: int,
) -> Attachment | None:
    return (
        db.query(Attachment)
        .filter(
            Attachment.id == attachment_id
        )
        .first()
    )


def get_page_attachments(
    db: Session,
    page_id: int,
) -> list[Attachment]:
    return (
        db.query(Attachment)
        .filter(
            Attachment.page_id == page_id
        )
        .order_by(
            Attachment.created_at.desc()
        )
        .all()
    )


def delete_attachment(
    db: Session,
    attachment: Attachment,
) -> None:
    db.delete(attachment)
    db.commit()