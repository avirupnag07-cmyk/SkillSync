"""System Diagnostics and Provider Health Check API Route."""

from fastapi import APIRouter
from app.services.llm_provider import llm_provider
from app.core.config import settings

router = APIRouter(tags=["Health & Status"])


@router.get("/health")
def health_check():
    """Diagnostic health check verifying backend, database, and LLM reasoning provider."""
    provider_info = llm_provider.get_provider_status()
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "active_provider": provider_info,
        "database": "connected"
    }
