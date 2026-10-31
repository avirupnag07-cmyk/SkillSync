"""Market Intelligence and Role Comparison Schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field


class RankedSkillItem(BaseModel):
    id: str
    name: str
    category: str
    category_name: str
    frequency: int
    demand_percentage: float
    mandatory_ratio: float
    weight: float


class CategoryShareItem(BaseModel):
    category_id: str
    name: str
    count: int
    percentage: float


class MarketOverviewResponse(BaseModel):
    total_jobs_analyzed: int
    unique_skills_tracked: int
    top_skills: List[RankedSkillItem]
    category_distribution: List[CategoryShareItem]
    emerging_technologies: List[dict]


class RoleDetail(BaseModel):
    key: str
    title: str
    description: str
    average_salary: str
    demand_trend: str
    total_core_skills: int
    unique_skills: List[dict]


class RoleComparisonResponse(BaseModel):
    role_a: RoleDetail
    role_b: RoleDetail
    shared_skills: List[dict]
    overlap_percentage: float
    transition_difficulty_score: float
    recommendation: str
