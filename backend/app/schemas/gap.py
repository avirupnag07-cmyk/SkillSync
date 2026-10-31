"""Skill Gap Analysis and Compatibility Response Schemas."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class GapAnalysisRequest(BaseModel):
    profile_id: Optional[str] = None
    job_id: Optional[str] = None
    # Or direct raw inputs
    raw_resume_text: Optional[str] = None
    raw_job_description: Optional[str] = None
    candidate_skills: Optional[List[dict]] = None
    candidate_experience_years: Optional[float] = 3.0
    required_experience_years: Optional[float] = 3.0
    job_title: Optional[str] = "Target Role"
    candidate_name: Optional[str] = "Candidate"


class GapAnalysisResponse(BaseModel):
    id: Optional[str] = None
    overall_score: float
    mandatory_score: float
    preferred_score: float
    experience_score: float
    alignment_tier: str
    executive_summary: str
    disclaimer: str
    counts: dict
    matched_skills: List[dict]
    partially_matched_skills: List[dict]
    missing_mandatory_skills: List[dict]
    missing_preferred_skills: List[dict]
    unverified_skills: List[dict]
    category_breakdown: List[dict]
    audit_trail: Optional[List[dict]] = None
    provider_info: Optional[dict] = None
