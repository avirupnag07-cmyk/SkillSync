"""Job Postings and Search Pydantic Schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field


class PasteJobRequest(BaseModel):
    title: str = "Software Engineer"
    company: Optional[str] = "Confidential Company"
    location: Optional[str] = "Remote"
    required_experience_years: Optional[int] = 3
    salary_range: Optional[str] = None
    description: str


class JobOut(BaseModel):
    id: str
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    source: str
    salary_range: Optional[str] = None
    required_experience_years: int
    description: str
    url: Optional[str] = None
    extracted_skills: List[dict] = Field(default_factory=list)
    skills_count: int = 0
