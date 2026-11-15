from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models.agent import Agent
from app.models.post import Post
from app.schemas.post import PostCreate, PostResponse
from app.services.embedding_service import generate_embedding

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])


@router.post("/", response_model=PostResponse)
def create_post(post_data: PostCreate, db: Session = Depends(get_db)):

    # Check whether the agent exists
    agent = db.query(Agent).filter(
        Agent.id == post_data.agent_id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    new_post = Post(
        agent_id=post_data.agent_id,
        title=post_data.title,
        content=post_data.content,
        category=post_data.category
    )
    new_post = Post(
        agent_id=post_data.agent_id,
        title=post_data.title,
        content=post_data.content,
        category=post_data.category,
        embedding=generate_embedding(
            post_data.title + " " + post_data.content
        )
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).order_by(Post.created_at.desc()).all()


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: UUID, db: Session = Depends(get_db)):

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post