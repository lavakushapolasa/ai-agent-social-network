
import uuid

from sqlalchemy import Column, String, Text, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from pgvector.sqlalchemy import Vector

from app.database import Base


class Agent(Base):
    __tablename__ = "agents"
    embedding = Column(Vector(384), nullable=True)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    company_name = Column(String(255), nullable=False)
    industry_category = Column(String(100), nullable=False)

    webhook_url = Column(Text, nullable=False)
    interest_manifesto = Column(Text, nullable=False)

    trust_score = Column(Float, default=1.0)
    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
