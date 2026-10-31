"""Skill Extraction and Normalization Agent.

Classifies technologies, maps aliases to ontology IDs, and separates
mandatory specifications from preferred bonus qualifications.
"""

import datetime
from app.agents.state import AgentState
from app.services.skill_extractor import extract_skills_from_text


def skill_extraction_agent(state: AgentState) -> AgentState:
    """Agent step: Extract and categorize requirements from the target job posting."""
    state.active_agent = "skill_extraction_agent"
    timestamp = datetime.datetime.utcnow().isoformat()

    if state.target_job:
        job_desc = state.target_job.get("description", "")
        extracted_skills = extract_skills_from_text(job_desc, default_mandatory=True, is_job_posting=True)
        state.extracted_job_skills = extracted_skills
        state.target_job["extracted_skills"] = extracted_skills
    elif not state.extracted_job_skills:
        state.errors.append("skill_extraction_agent: No target job available to extract skills from.")

    state.audit_trail.append({
        "agent": "skill_extraction_agent",
        "timestamp": timestamp,
        "action": "extracted_job_skills",
        "total_skills": len(state.extracted_job_skills),
        "mandatory_count": sum(1 for s in state.extracted_job_skills if s.get("is_mandatory", True))
    })

    return state
