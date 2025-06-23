from sqlalchemy.orm import Session
from app.models.comment import Comment
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
    return db_comment

def get_session_comments(db: Session, session_id: int):
    return db.query(Comment).filter(Comment.session_id == session_id).order_by(Comment.created_at).all()