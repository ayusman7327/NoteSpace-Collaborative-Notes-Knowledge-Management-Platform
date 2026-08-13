from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.attachment import AttachmentResponse
from app.services.attachment_service import (
    list_page_attachments,
    remove_page_attachment,
    upload_page_attachment,
)


router = APIRouter(
    prefix="/attachments",
    tags=["Attachments"],
)


@router.post(
    "/page/{page_id}",
    response_model=AttachmentResponse,
)
async def upload_attachment_route(
    page_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await upload_page_attachment(
        db=db,
        page_id=page_id,
        user_id=current_user.id,
        file=file,
    )


@router.get(
    "/page/{page_id}",
    response_model=list[AttachmentResponse],
)
def get_page_attachments_route(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_page_attachments(
        db=db,
        page_id=page_id,
        user_id=current_user.id,
    )


@router.delete(
    "/{attachment_id}",
)
def delete_attachment_route(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return remove_page_attachment(
        db=db,
        attachment_id=attachment_id,
        user_id=current_user.id,
    )