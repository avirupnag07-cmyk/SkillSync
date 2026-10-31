"""Skill Gap Analysis and Explainable Compatibility Agent.

Performs deterministic multi-factor requirement matching, category breakdowns,
and provides transparent rationale without hallucinations.
"""

import datetime
from app.agents.state import AgentState
from app.services.compatibility_scorer import compute_compatibility_score


def skill_gap_analysis_agent(state: AgentState) -> AgentState:
    """Agent step: Compare candidate skills against job requirements."""
    state.active_agent = "skill_gap_analysis_agent"
    timestamp = datetime.datetime.utcnow().isoformat()

    candidate_skills = state.extracted_candidate_skills or []
    job_skills = state.extracted_job_skills or []

    candidate_exp = 3.0
    if state.candidate_profile:
        candidate_exp = float(state.candidate_profile.get("experience_years", 3.0))

    required_exp = 3.0
    if state.target_job:
        required_exp = float(state.target_job.get("required_experience_years", 3.0))

    gap_result = compute_compatibility_score(
        candidate_skills=candidate_skills,
        job_skills=job_skills,
        candidate_experience_years=candidate_exp,
        required_experience_years=required_exp
    )

    state.gap_analysis_result = gap_result

    state.audit_trail.append({
        "agent": "skill_gap_analysis_agent",
        "timestamp": timestamp,
        "action": "computed_gap_analysis",
        "overall_score": gap_result["overall_score"],
        "alignment_tier": gap_result["alignment_tier"],
        "missing_mandatory": len(gap_result["missing_mandatory_skills"])
    })

    return state
