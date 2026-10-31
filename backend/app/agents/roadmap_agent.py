"""Learning Recommendation and Roadmap Agent.

Maps identified skill deficits into an actionable, weekly progressive curriculum
linking verified official documentation, free university courses, and project milestones.
"""

import datetime
from app.agents.state import AgentState
from app.services.roadmap_generator import generate_learning_roadmap


def learning_recommendation_agent(state: AgentState) -> AgentState:
    """Agent step: Generate adaptive learning plan based on gap analysis output."""
    state.active_agent = "learning_recommendation_agent"
    timestamp = datetime.datetime.utcnow().isoformat()

    missing_skills = []
    if state.gap_analysis_result:
        missing_skills.extend(state.gap_analysis_result.get("missing_mandatory_skills", []))
        missing_skills.extend(state.gap_analysis_result.get("missing_preferred_skills", []))
        missing_skills.extend(state.gap_analysis_result.get("partially_matched_skills", []))

    role_title = "Target Engineering Role"
    if state.target_job:
        role_title = state.target_job.get("title", role_title)

    roadmap = generate_learning_roadmap(
        missing_skills=missing_skills,
        target_role_title=role_title,
        duration_weeks=6
    )

    state.learning_roadmap_result = roadmap

    state.audit_trail.append({
        "agent": "learning_recommendation_agent",
        "timestamp": timestamp,
        "action": "generated_learning_roadmap",
        "weeks": roadmap["duration_weeks"],
        "target_role": role_title
    })

    return state
