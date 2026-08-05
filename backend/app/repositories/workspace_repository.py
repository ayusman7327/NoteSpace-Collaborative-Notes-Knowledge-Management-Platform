from sqlalchemy.orm import Session

from app.models.workspace import Workspace, WorkspaceMember, WorkspaceRole


def create_workspace(
    db: Session,
    name: str,
    owner_id: int
):
    workspace = Workspace(
        name=name,
        owner_id=owner_id
    )

    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    member = WorkspaceMember(
        workspace_id=workspace.id,
        user_id=owner_id,
        role=WorkspaceRole.OWNER
    )

    db.add(member)
    db.commit()

    return workspace


def get_user_workspaces(
    db: Session,
    user_id: int
):
    return (
        db.query(Workspace)
        .join(
            WorkspaceMember,
            Workspace.id == WorkspaceMember.workspace_id
        )
        .filter(
            WorkspaceMember.user_id == user_id
        )
        .all()
    )