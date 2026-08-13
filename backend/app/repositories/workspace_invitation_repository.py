from sqlalchemy.orm import Session

from app.models.workspace_invitation import WorkspaceInvitation


def create_invitation(
    db: Session,
    workspace_id: int,
    invited_by: int,
    email: str,
    role: str,
):
    invitation = WorkspaceInvitation(
        workspace_id=workspace_id,
        invited_by=invited_by,
        email=email.lower().strip(),
        role=role,
        status="pending",
    )

    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    return invitation


def get_invitation_by_id(
    db: Session,
    invitation_id: int,
):
    return (
        db.query(WorkspaceInvitation)
        .filter(
            WorkspaceInvitation.id == invitation_id
        )
        .first()
    )


def get_pending_invitation(
    db: Session,
    workspace_id: int,
    email: str,
):
    return (
        db.query(WorkspaceInvitation)
        .filter(
            WorkspaceInvitation.workspace_id == workspace_id,
            WorkspaceInvitation.email == email.lower().strip(),
            WorkspaceInvitation.status == "pending",
        )
        .first()
    )


def get_workspace_invitations(
    db: Session,
    workspace_id: int,
):
    return (
        db.query(WorkspaceInvitation)
        .filter(
            WorkspaceInvitation.workspace_id == workspace_id
        )
        .order_by(
            WorkspaceInvitation.created_at.desc()
        )
        .all()
    )


def get_user_pending_invitations(
    db: Session,
    email: str,
):
    return (
        db.query(WorkspaceInvitation)
        .filter(
            WorkspaceInvitation.email == email.lower().strip(),
            WorkspaceInvitation.status == "pending",
        )
        .order_by(
            WorkspaceInvitation.created_at.desc()
        )
        .all()
    )


def update_invitation_status(
    db: Session,
    invitation: WorkspaceInvitation,
    new_status: str,
):
    invitation.status = new_status

    db.commit()
    db.refresh(invitation)

    return invitation


def accept_invitation(
    db: Session,
    invitation: WorkspaceInvitation,
):
    invitation.status = "accepted"

    db.commit()
    db.refresh(invitation)

    return invitation


def reject_invitation(
    db: Session,
    invitation: WorkspaceInvitation,
):
    invitation.status = "rejected"

    db.commit()
    db.refresh(invitation)

    return invitation


def cancel_invitation(
    db: Session,
    invitation: WorkspaceInvitation,
):
    invitation.status = "cancelled"

    db.commit()
    db.refresh(invitation)

    return invitation


def delete_invitation(
    db: Session,
    invitation: WorkspaceInvitation,
):
    db.delete(invitation)
    db.commit()

    return True