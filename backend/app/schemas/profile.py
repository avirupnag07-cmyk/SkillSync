"""Candidate Profile and Skill Pydantic Schemas."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SkillItem(BaseModel):
    id: str
    name: str
    category: str
    category_name: Optional[str] = None
    weight: Optional[float] = 1.5
    verified: Optional[bool] = True
    years_experience: Optional[float] = None


class ExperienceItem(BaseModel):
    company: str
    role: str
    duration: str
    description: Optional[str] = None
    skills_used: List[str] = Field(default_factory=list)


class ProjectItem(BaseModel):
    title: str
    description: str
    url: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)


class EducationItem(BaseModel):
    institution: str
    degree: str
    graduation_year: Optional[str] = None


class ProfileCreateOrUpdate(BaseModel):
    name: str = "Candidate"
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    experience_years: float = 2.0
    bio: Optional[str] = None
    skills: List[SkillItem] = Field(default_factory=list)
    experiences: List[ExperienceItem] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)


class ProfileOut(BaseModel):
    id: str
    user_id: Optional[str] = None
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    experience_years: float
    bio: Optional[str] = None
    skills: List[dict]
    experiences: List[dict]
    projects: List[dict]
    education: List[dict]
    created_at: Optional[str] = None
