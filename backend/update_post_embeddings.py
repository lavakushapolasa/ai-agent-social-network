
from app.database import SessionLocal
from app.models.agent import Agent
from app.models.post import Post
from app.services.embedding_service import generate_embedding

db = SessionLocal()

try:
    posts = db.query(Post).filter(Post.embedding.is_(None)).all()

    for post in posts:
        post.embedding = generate_embedding(
            post.title + " " + post.content
        )
        print("Updated:", post.title)

    db.commit()
    print("All missing post embeddings updated!")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()

