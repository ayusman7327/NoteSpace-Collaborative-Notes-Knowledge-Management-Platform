from datetime import datetime
from pydantic import BaseModel


class PageVersionResponse(BaseModel):
    id: int
    page_id: int
    version_number: int
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True