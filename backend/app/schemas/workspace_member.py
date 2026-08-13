from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WorkspaceMemberCreate(BaseModel):
    user_id: int

    role: str = Field(
        default="viewer",
        pattern="^(owner|editor|viewer)$",
    )


class WorkspaceMemberRoleUpdate(BaseModel):
    role: str = Field(
        pattern="^(owner|editor|viewer)$"
    )


class WorkspaceMemberResponse(BaseModel):
    id: int
    workspace_id: int
    user_id: int
    role: str
    joined_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )