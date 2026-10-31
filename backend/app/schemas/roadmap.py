"""Learning Roadmap Schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field


class TaskItem(BaseModel):
    id: str
    description: str
    completed: bool = False


class WeekPlan(BaseModel):
    week_number: int
    title: str
    goal: str
    skills: List[dict] = Field(default_factory=list)
    documentation_links: List[str] = Field(default_factory=list)
    free_resources: List[str] = Field(default_factory=list)
    project_milestone: str
    tasks: List[TaskItem] = Field(default_factory=list)


class RoadmapGenerateRequest(BaseModel):
    gap_analysis_id: Optional[str] = None
    target_role: Optional[str] = "Target Engineering Role"
    duration_weeks: Optional[int] = 6
    missing_skills: Optional[List[dict]] = None


class RoadmapResponse(BaseModel):
    id: Optional[str] = None
    title: str
    target_role: str
    duration_weeks: int
    total_skills: int
    weeks: List[WeekPlan]
    created_at: Optional[str] = None


class TaskToggleRequest(BaseModel):
    week_number: int
    task_id: str
    completed: bool
