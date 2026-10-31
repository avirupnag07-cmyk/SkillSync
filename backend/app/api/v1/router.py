"""Unified API Router Aggregator for v1 Endpoints."""

from fastapi import APIRouter
from app.api.v1 import (
    auth,
    profile,
    jobs,
    skills,
    gap,
    market,
    roadmap,
    comparison,
    reports,
    health,
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(profile.router)
api_router.include_router(jobs.router)
api_router.include_router(skills.router)
api_router.include_router(gap.router)
api_router.include_router(market.router)
api_router.include_router(roadmap.router)
api_router.include_router(comparison.router)
api_router.include_router(reports.router)
