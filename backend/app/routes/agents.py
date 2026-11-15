
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentResponse

from app.services.embedding_service import generate_embedding

router = APIRouter(prefix="/api/v1/agents", tags=["Agents"])


@router.post("/register", response_model=AgentResponse)
def register_agent(agent_data: AgentCreate, db: Session = Depends(get_db)):
    new_agent = Agent(
        company_name=agent_data.company_name,
        industry_category=agent_data.industry_category,
        webhook_url=str(agent_data.webhook_url),
        interest_manifesto=agent_data.interest_manifesto
    )

    new_agent = Agent(
        company_name=agent_data.company_name,
        industry_category=agent_data.industry_category,
        webhook_url=str(agent_data.webhook_url),
        interest_manifesto=agent_data.interest_manifesto,
        embedding=generate_embedding(agent_data.interest_manifesto)
    )
    

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return new_agent


@router.get("/", response_model=list[AgentResponse])
def get_agents(db: Session = Depends(get_db)):
    return db.query(Agent).all()


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: UUID, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent


@router.delete("/{agent_id}")
def deactivate_agent(agent_id: UUID, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent.is_active = False
    db.commit()

    return {
        "message": "Agent deactivated successfully",
        "agent_id": str(agent.id),
        "company_name": agent.company_name,
        "is_active": agent.is_active
    }
