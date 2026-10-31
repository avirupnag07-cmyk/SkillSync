"""Agent State Definitions for the SkillSync Orchestration Framework.

Defines typed state models tracking intermediate outputs across all specialized agents.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """Unified state container passed between agents in the workflow graph."""

    # Context & Inputs
    session_id: str = "default_session"
    raw_resume_text: Optional[str] = None
    resume_filename: Optional[str] = None
    job_query: Optional[str] = None
    target_job: Optional[dict] = None
    candidate_profile: Optional[dict] = None

    # Intermediate / Agent Outputs
    extracted_candidate_skills: List[dict] = Field(default_factory=list)
    extracted_job_skills: List[dict] = Field(default_factory=list)
    gap_analysis_result: Optional[dict] = None
    learning_roadmap_result: Optional[dict] = None
    market_intelligence_result: Optional[dict] = None
    role_comparison_result: Optional[dict] = None

    # Telemetry and Execution History
    audit_trail: List[dict] = Field(default_factory=list)
    active_agent: Optional[str] = None
    errors: List[str] = Field(default_factory=list)
    provider_info: Optional[dict] = None
