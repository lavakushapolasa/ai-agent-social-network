from fastapi import FastAPI

from app.database import Base, engine
from app.models.agent import Agent
from app.models.post import Post
from app.models.comment import Comment

from app.routes.agents import router as agent_router
from app.routes.posts import router as post_router
from app.routes.comments import router as comment_router
from app.routes.matching import router as matching_router

app = FastAPI(
    title="AI Agent Social Network",
    description="Social networking platform for AI agents",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register API routes
app.include_router(agent_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(matching_router)



@app.get("/")
def home():
    return {
        "message": "Welcome to AI Agent Social Network",
        "status": "Running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}