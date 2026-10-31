"""Job Search and Ingestion Agent.

Performs remote job discovery, normalizes job postings from public APIs,
and prepares requirements text for semantic skill extraction.
"""

import datetime
from app.agents.state import AgentState
from app.services.job_api_service import search_all_jobs


def job_search_agent(state: AgentState) -> AgentState:
    """Agent step: Discover and normalize job postings based on search intent."""
    state.active_agent = "job_search_agent"
    timestamp = datetime.datetime.utcnow().isoformat()

    query = state.job_query or "software"
    discovered_jobs = search_all_jobs(query=query)

    # If target job is not yet specified, set target to top result
    if not state.target_job and discovered_jobs:
        state.target_job = discovered_jobs[0]

    state.audit_trail.append({
        "agent": "job_search_agent",
        "timestamp": timestamp,
        "action": "queried_jobs",
        "query": query,
        "results_found": len(discovered_jobs)
    })

    return state
