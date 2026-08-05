from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PageVersionResponse(BaseModel):
    id: int
    page_id: int
    content_snapshot: str
    edited_by: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )