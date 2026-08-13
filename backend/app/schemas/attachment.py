from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)


class AttachmentResponse(BaseModel):
    id: int
    page_id: int
    uploaded_by: int
    file_name: str
    stored_name: str
    file_type: str | None
    file_size: int
    file_url: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )