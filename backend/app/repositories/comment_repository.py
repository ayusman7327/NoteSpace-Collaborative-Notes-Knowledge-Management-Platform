from sqlalchemy.orm import Session

from app.models.comment import Comment


def create_comment(
    db: Session,
    page_id: int,
    user_id: int,
    content: str,
) -> Comment:
    comment = Comment(
        page_id=page_id,
        user_id=user_id,
        content=content,
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


def get_comment_by_id(
    db: Session,
    comment_id: int,
) -> Comment | None:
    return (
        db.query(Comment)
        .filter(
            Comment.id == comment_id
        )
        .first()
    )


def get_page_comments(
    db: Session,
    page_id: int,
) -> list[Comment]:
    return (
        db.query(Comment)
        .filter(
            Comment.page_id == page_id
        )
        .order_by(
            Comment.created_at.desc()
        )
        .all()
    )


def update_comment(
    db: Session,
    comment: Comment,
    content: str,
) -> Comment:
    comment.content = content

    db.commit()
    db.refresh(comment)

    return comment


def resolve_comment(
    db: Session,
    comment: Comment,
) -> Comment:
    comment.is_resolved = True

    db.commit()
    db.refresh(comment)

    return comment


def reopen_comment(
    db: Session,
    comment: Comment,
) -> Comment:
    comment.is_resolved = False

    db.commit()
    db.refresh(comment)

    return comment


def delete_comment(
    db: Session,
    comment: Comment,
) -> None:
    db.delete(comment)
    db.commit()