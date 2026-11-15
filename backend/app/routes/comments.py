
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models.agent import Agent
from app.models.post import Post
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentResponse

router = APIRouter(
    prefix="/api/v1/comments",
    tags=["Comments"]
)


@router.post("/", response_model=CommentResponse)
def create_comment(
    comment_data: CommentCreate,
    db: Session = Depends(get_db)
):

    post = db.query(Post).filter(
        Post.id == comment_data.post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    agent = db.query(Agent).filter(
        Agent.id == comment_data.agent_id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    new_comment = Comment(
        post_id=comment_data.post_id,
        agent_id=comment_data.agent_id,
        content=comment_data.content
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.get("/", response_model=list[CommentResponse])
def get_comments(db: Session = Depends(get_db)):
    return db.query(Comment).order_by(
        Comment.created_at.desc()
    ).all()


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(
    comment_id: UUID,
    db: Session = Depends(get_db)
):

    comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    return comment
