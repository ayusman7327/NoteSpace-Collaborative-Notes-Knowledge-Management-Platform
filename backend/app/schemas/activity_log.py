from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ActivityLogResponse(BaseModel):
    id: int
    workspace_id: int
    page_id: int | None
    user_id: int
    action: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )