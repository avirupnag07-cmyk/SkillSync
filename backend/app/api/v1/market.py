"""Market Intelligence and Demand Analytics API Routes."""

from fastapi import APIRouter
from app.schemas.market import MarketOverviewResponse
from app.services.market_analyzer import compute_market_skill_demand, ROLE_TAXONOMY

router = APIRouter(prefix="/market", tags=["Market Intelligence"])


@router.get("/overview", response_model=MarketOverviewResponse)
def get_market_overview():
    """Retrieve industry-wide skill demand rankings, category distributions, and growth trajectories."""
    market_data = compute_market_skill_demand()
    return MarketOverviewResponse(
        total_jobs_analyzed=market_data["total_jobs_analyzed"],
        unique_skills_tracked=market_data["unique_skills_tracked"],
        top_skills=market_data["top_skills"],
        category_distribution=market_data["category_distribution"],
        emerging_technologies=market_data["emerging_technologies"]
    )


@router.get("/roles")
def get_available_roles():
    """List benchmark engineering roles available for comparative analysis."""
    roles = []
    for k, v in ROLE_TAXONOMY.items():
        roles.append({
            "key": k,
            "title": v["title"],
            "description": v["description"],
            "average_salary": v["average_salary"],
            "demand_trend": v["demand_trend"]
        })
    return roles
