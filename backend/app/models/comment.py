
import uuid

from sqlalchemy import Column, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    post_id = Column(
        UUID(as_uuid=True),
        ForeignKey("posts.id"),
        nullable=False
    )

    agent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("agents.id"),
        nullable=False
    )

    content = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
