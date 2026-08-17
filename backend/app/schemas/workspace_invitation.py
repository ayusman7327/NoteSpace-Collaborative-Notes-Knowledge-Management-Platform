from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class WorkspaceInvitationCreate(BaseModel):
    email: EmailStr
    role: str = "member"


class WorkspaceInvitationResponse(BaseModel):
    id: int
    workspace_id: int
    email: EmailStr
    role: str
    status: str
    invited_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkspaceInvitationAccept(BaseModel):
    invitation_id: int


class WorkspaceInvitationReject(BaseModel):
    invitation_id: int