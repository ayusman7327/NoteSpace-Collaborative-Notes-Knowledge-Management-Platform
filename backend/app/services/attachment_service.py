import os
import uuid

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.repositories.attachment_repository import (
    create_attachment,
    delete_attachment,
    get_attachment_by_id,
    get_page_attachments,
)
from app.repositories.page_repository import get_page_by_id
from app.services.page_service import (
    check_edit_permission,
    check_workspace_membership,
)


UPLOAD_DIRECTORY = "uploads"

MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_CONTENT_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
    "application/pdf",
    "text/plain",
    "text/markdown",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def ensure_upload_directory():
    os.makedirs(
        UPLOAD_DIRECTORY,
        exist_ok=True,
    )


async def upload_page_attachment(
    db: Session,
    page_id: int,
    user_id: int,
    file: UploadFile,
):
    page = get_page_by_id(
        db=db,
        page_id=page_id,
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found",
        )

    membership = check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id,
    )

    check_edit_permission(
        membership
    )

    if (
        file.content_type
        not in ALLOWED_CONTENT_TYPES
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type is not supported",
        )

    file_content = await file.read()

    file_size = len(
        file_content
    )

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be 10 MB or less",
        )

    ensure_upload_directory()

    extension = os.path.splitext(
        file.filename or ""
    )[1]

    stored_name = (
        f"{uuid.uuid4().hex}{extension}"
    )

    stored_path = os.path.join(
        UPLOAD_DIRECTORY,
        stored_name,
    )

    with open(
        stored_path,
        "wb",
    ) as destination:
        destination.write(
            file_content
        )

    return create_attachment(
        db=db,
        page_id=page_id,
        uploaded_by=user_id,
        file_name=file.filename
        or stored_name,
        stored_name=stored_name,
        file_type=file.content_type,
        file_size=file_size,
        file_url=f"/uploads/{stored_name}",
    )


def list_page_attachments(
    db: Session,
    page_id: int,
    user_id: int,
):
    page = get_page_by_id(
        db=db,
        page_id=page_id,
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

    return get_page_attachments(
        db=db,
        page_id=page_id,
    )


def remove_page_attachment(
    db: Session,
    attachment_id: int,
    user_id: int,
):
    attachment = get_attachment_by_id(
        db=db,
        attachment_id=attachment_id,
    )

    if attachment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found",
        )

    page = get_page_by_id(
        db=db,
        page_id=attachment.page_id,
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found",
        )

    membership = check_workspace_membership(
        db=db,
        workspace_id=page.workspace_id,
        user_id=user_id,
    )

    check_edit_permission(
        membership
    )

    file_path = os.path.join(
        UPLOAD_DIRECTORY,
        attachment.stored_name,
    )

    if os.path.exists(
        file_path
    ):
        os.remove(
            file_path
        )

    delete_attachment(
        db=db,
        attachment=attachment,
    )

    return {
        "message": "Attachment deleted successfully"
    }