from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PageCreate(BaseModel):
    workspace_id: int
    parent_page_id: int | None = None
    title: str
    content: str = ""


class PageResponse(BaseModel):
    id: int
    workspace_id: int
    parent_page_id: int | None
    title: str
    content: str
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )