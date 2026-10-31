"""Market Intelligence and Role Comparison Agent.

Extracts aggregate skill demand distributions and benchmark role comparisons
to provide broader macroeconomic context to the candidate.
"""

import datetime
from app.agents.state import AgentState
from app.services.market_analyzer import compute_market_skill_demand, compare_engineering_roles


def market_intelligence_agent(state: AgentState) -> AgentState:
    """Agent step: Aggregate market trends and generate cross-role benchmark metrics."""
    state.active_agent = "market_intelligence_agent"
    timestamp = datetime.datetime.utcnow().isoformat()

    market_data = compute_market_skill_demand()
    comparison_data = compare_engineering_roles("ai_engineer", "data_scientist")

    state.market_intelligence_result = market_data
    state.role_comparison_result = comparison_data

    state.audit_trail.append({
        "agent": "market_intelligence_agent",
        "timestamp": timestamp,
        "action": "aggregated_market_intelligence",
        "jobs_analyzed": market_data["total_jobs_analyzed"],
        "top_skill": market_data["top_skills"][0]["name"] if market_data["top_skills"] else None
    })

    return state
