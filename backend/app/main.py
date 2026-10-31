"""SkillSync FastAPI Application Entrypoint."""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.api.v1.router import api_router
from app.services.llm_provider import llm_provider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("skillsync")

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Execute startup and shutdown routines."""
    logger.info("Initializing SkillSync database tables...")
    init_db()
    provider = llm_provider.get_provider_status()
    logger.info(f"SkillSync Online. Active reasoning provider: {provider['badge_label']}")
    yield
    logger.info("SkillSync shutting down.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Real-time AI Skill Gap Intelligence & Learning Recommendation Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    """Welcome and quick API index."""
    return {
        "message": "Welcome to SkillSync API - AI Skill Gap Intelligence Platform",
        "documentation": "/docs",
        "health": "/api/v1/health",
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
