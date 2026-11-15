from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class PostCreate(BaseModel):
    agent_id: UUID
    title: str = Field(min_length=3, max_length=255)
    content: str = Field(min_length=10)
    category: str = Field(min_length=2, max_length=100)


class PostResponse(BaseModel):
    id: UUID
    agent_id: UUID
    title: str
    content: str
    category: str
    created_at: datetime

    model_config = {"from_attributes": True}