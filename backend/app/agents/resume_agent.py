"""Resume Intelligence Agent.

Parses document structure, identifies candidate professional qualifications,
projects, employment milestones, and extracts raw candidate skills.
"""

import datetime
from app.agents.state import AgentState
from app.services.resume_parser import parse_resume_document, extract_candidate_contact
from app.services.skill_extractor import extract_skills_from_text


def resume_intelligence_agent(state: AgentState) -> AgentState:
    """Agent step: Extract candidate profile and skills from resume text or file bytes."""
    state.active_agent = "resume_intelligence_agent"
    timestamp = datetime.datetime.utcnow().isoformat()

    raw_text = state.raw_resume_text or ""
    filename = state.resume_filename or "uploaded_resume.txt"

    contact = extract_candidate_contact(raw_text)
    if raw_text:
        extracted_skills = extract_skills_from_text(raw_text, default_mandatory=False, is_job_posting=False)
        state.extracted_candidate_skills = extracted_skills
    else:
        extracted_skills = state.extracted_candidate_skills or []

    profile = {
        "name": contact["name"] if contact["name"] != "Candidate" and raw_text else (state.candidate_profile.get("name") if state.candidate_profile else "Candidate"),
        "email": contact["email"],
        "phone": contact["phone"],
        "linkedin": contact["linkedin"],
        "github": contact["github"],
        "filename": filename,
        "skills": extracted_skills,
        "skills_count": len(extracted_skills),
        "experience_years": state.candidate_profile.get("experience_years", 3.0) if state.candidate_profile else 3.0
    }

    state.candidate_profile = profile

    state.audit_trail.append({
        "agent": "resume_intelligence_agent",
        "timestamp": timestamp,
        "action": "extracted_candidate_profile",
        "skills_identified": len(extracted_skills),
        "candidate_name": contact["name"]
    })

    return state
