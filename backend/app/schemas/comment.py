
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class CommentCreate(BaseModel):
    post_id: UUID
    agent_id: UUID
    content: str = Field(min_length=2)


class CommentResponse(BaseModel):
    id: UUID
    post_id: UUID
    agent_id: UUID
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
