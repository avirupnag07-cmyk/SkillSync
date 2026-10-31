"""Unit tests for LangGraph Agent Orchestration and Workflow Execution."""

from app.agents.state import AgentState
from app.agents.graph import skillsync_workflow


def test_agent_workflow_execution():
    resume_sample = "Experienced Senior Developer skilled in Python, FastAPI, Docker, and PostgreSQL with 4 years experience."
    job_sample = {
        "title": "Backend AI Specialist",
        "company": "NextGen Labs",
        "description": "Minimum Qualifications: Python, FastAPI, Docker. Preferred Qualifications: PyTorch, Kubernetes.",
        "required_experience_years": 3
    }

    state = AgentState(
        session_id="test-session-123",
        raw_resume_text=resume_sample,
        target_job=job_sample
    )

    final_state = skillsync_workflow.run(state)

    # Validate agent pipeline ran completely
    assert final_state.active_agent == "completed"
    assert len(final_state.audit_trail) >= 4

    # Validate extracted outputs
    assert len(final_state.extracted_candidate_skills) >= 3
    assert len(final_state.extracted_job_skills) >= 3

    # Validate gap analysis generated
    assert final_state.gap_analysis_result is not None
    assert final_state.gap_analysis_result["overall_score"] > 50.0

    # Validate learning roadmap generated
    assert final_state.learning_roadmap_result is not None
    assert len(final_state.learning_roadmap_result["weeks"]) >= 2
