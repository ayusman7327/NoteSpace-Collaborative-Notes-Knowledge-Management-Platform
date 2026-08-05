from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PageCreate(BaseModel):
    workspace_id: int
    parent_page_id: int | None = None
    title: str = Field(
        min_length=1,
        max_length=200
    )
    content: str = ""


class PageUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )
    content: str | None = None


class PageResponse(BaseModel):
    id: int
    workspace_id: int
    parent_page_id: int | None
    title: str
    content: str
    created_by: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True
    )