"""Cross-Role Career Comparison API Routes."""

from fastapi import APIRouter, Query
from app.schemas.market import RoleComparisonResponse
from app.services.market_analyzer import compare_engineering_roles

router = APIRouter(prefix="/comparison", tags=["Role Comparison"])


@router.get("/compare", response_model=RoleComparisonResponse)
def compare_roles(
    role_a: str = Query(default="ai_engineer", description="First role key (e.g. ai_engineer, data_scientist)"),
    role_b: str = Query(default="data_scientist", description="Second role key (e.g. data_engineer, fullstack_engineer)")
):
    """Compare skill requirements, shared foundations, and transition difficulty between roles."""
    comparison = compare_engineering_roles(role_a, role_b)
    return RoleComparisonResponse(
        role_a=comparison["role_a"],
        role_b=comparison["role_b"],
        shared_skills=comparison["shared_skills"],
        overlap_percentage=comparison["overlap_percentage"],
        transition_difficulty_score=comparison["transition_difficulty_score"],
        recommendation=comparison["recommendation"]
    )
