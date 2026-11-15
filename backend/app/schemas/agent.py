
from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID


class AgentCreate(BaseModel):
    company_name: str = Field(min_length=2, max_length=255)
    industry_category: str = Field(min_length=2, max_length=100)
    webhook_url: HttpUrl
    interest_manifesto: str = Field(min_length=10)


class AgentResponse(BaseModel):
    id: UUID
    company_name: str
    industry_category: str
    webhook_url: str
    interest_manifesto: str
    trust_score: float
    is_active: bool

    model_config = {"from_attributes": True}
