from sqlalchemy.orm import Session

from app.models.workspace_member import WorkspaceMember


def create_workspace_member(
    db: Session,
    workspace_id: int,
    user_id: int,
    role: str,
) -> WorkspaceMember:
    member = WorkspaceMember(
        workspace_id=workspace_id,
        user_id=user_id,
        role=role,
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


def get_workspace_member(
    db: Session,
    workspace_id: int,
    user_id: int,
) -> WorkspaceMember | None:
    return (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        )
        .first()
    )


def get_workspace_member_by_id(
    db: Session,
    member_id: int,
) -> WorkspaceMember | None:
    return (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.id == member_id
        )
        .first()
    )


def get_workspace_members(
    db: Session,
    workspace_id: int,
) -> list[WorkspaceMember]:
    return (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id
        )
        .order_by(
            WorkspaceMember.joined_at.asc()
        )
        .all()
    )


def update_workspace_member_role(
    db: Session,
    member: WorkspaceMember,
    role: str,
) -> WorkspaceMember:
    member.role = role

    db.commit()
    db.refresh(member)

    return member


def remove_workspace_member(
    db: Session,
    member: WorkspaceMember,
) -> None:
    db.delete(member)
    db.commit()