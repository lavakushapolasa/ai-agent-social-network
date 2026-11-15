
from app.database import SessionLocal
from app.models.agent import Agent
from app.services.embedding_service import generate_embedding

db = SessionLocal()

try:
    agents = db.query(Agent).filter(
        Agent.embedding.is_(None)
    ).all()

    for agent in agents:
        agent.embedding = generate_embedding(
            agent.interest_manifesto
        )
        print("Updated:", agent.company_name)

    db.commit()
    print("All missing agent embeddings updated!")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()
