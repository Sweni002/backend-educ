from sqlalchemy.orm import Session
from sqlalchemy import asc
from app.models.comment import Comment
from app.models.user import User
from app.schemas.comment import CommentCreate

def create_comment(db: Session, comment: CommentCreate, user_id: int):
    db_comment = Comment(
        session_id=comment.session_id,
        user_id=user_id,
        message=comment.message
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return {
        "id": db_comment.id,
        "session_id": db_comment.session_id,
        "user_id": db_comment.user_id,
        "message": db_comment.message,
        "created_at": db_comment.created_at,
        "user_name": db.query(User.name).filter(User.id == db_comment.user_id).scalar()  # ✅ Utilise name
    }

def get_session_comments(db: Session, session_id: int):
    results = (
        db.query(Comment, User.name)
        .join(User, User.id == Comment.user_id)
        .filter(Comment.session_id == session_id)
        .order_by(asc(Comment.created_at))
        .all()
    )

    return [
        {
            "id": comment.id,
            "session_id": comment.session_id,
            "user_id": comment.user_id,
            "message": comment.message,
            "created_at": comment.created_at,
            "user_name": name  # ✅ Affiche bien le name
        }
        for comment, name in results
    ]
