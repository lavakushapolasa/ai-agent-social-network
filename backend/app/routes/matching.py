
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db

router = APIRouter(
    prefix="/api/v1/matching",
    tags=["AI Relevance Matching"]
)


@router.get("/{post_id}")
def match_agents(post_id: str, db: Session = Depends(get_db)):

    query = text("""
        SELECT
            a.id AS agent_id,
            a.company_name,
            1 - (a.embedding <=> p.embedding) AS relevance_score
        FROM agents a
        CROSS JOIN posts p
        WHERE p.id = :post_id
          AND a.is_active = TRUE
          AND a.embedding IS NOT NULL
          AND p.embedding IS NOT NULL
          AND a.id != p.agent_id
        ORDER BY a.embedding <=> p.embedding
        LIMIT 10
    """)

    post_exists = db.execute(
        text("SELECT id FROM posts WHERE id = :post_id"),
        {"post_id": post_id}
    ).first()

    if not post_exists:
        raise HTTPException(status_code=404, detail="Post not found")

    results = db.execute(
        query,
        {"post_id": post_id}
    ).mappings().all()

    return {
        "post_id": post_id,
        "total_matches": len(results),
        "matches": [
            {
                "agent_id": str(row["agent_id"]),
                "company_name": row["company_name"],
                "relevance_score": round(float(row["relevance_score"]), 4)
            }
            for row in results
        ]
    }
