"""Personalized Learning Roadmap API Routes."""

import json
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_optional
from app.models.gap_analysis import SavedGapAnalysis
from app.models.roadmap import SavedRoadmap
from app.schemas.roadmap import RoadmapGenerateRequest, RoadmapResponse, TaskToggleRequest
from app.services.roadmap_generator import generate_learning_roadmap

router = APIRouter(prefix="/roadmap", tags=["Learning Roadmap"])


@router.post("/generate", response_model=RoadmapResponse)
def generate_roadmap_endpoint(
    payload: RoadmapGenerateRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_optional)
):
    """Generate an adaptive weekly upskilling roadmap mapped to identified competency gaps."""
    missing_skills = payload.missing_skills or []
    target_role = payload.target_role or "Target Engineering Role"

    # If gap_analysis_id provided, extract missing skills directly
    if payload.gap_analysis_id:
        gap_rec = db.query(SavedGapAnalysis).filter(SavedGapAnalysis.id == payload.gap_analysis_id).first()
        if gap_rec:
            res_data = json.loads(gap_rec.result_json)
            missing_skills = (
                res_data.get("missing_mandatory_skills", [])
                + res_data.get("missing_preferred_skills", [])
                + res_data.get("partially_matched_skills", [])
            )
            target_role = gap_rec.job_title or target_role

    roadmap_dict = generate_learning_roadmap(
        missing_skills=missing_skills,
        target_role_title=target_role,
        duration_weeks=payload.duration_weeks or 6
    )

    roadmap_id = f"rdm-{uuid.uuid4().hex[:10]}"
    saved_rdm = SavedRoadmap(
        id=roadmap_id,
        user_id=user["sub"],
        gap_analysis_id=payload.gap_analysis_id,
        title=roadmap_dict["title"],
        target_role=roadmap_dict["target_role"],
        duration_weeks=roadmap_dict["duration_weeks"],
        roadmap_json=json.dumps(roadmap_dict)
    )
    db.add(saved_rdm)
    db.commit()

    return RoadmapResponse(
        id=roadmap_id,
        title=roadmap_dict["title"],
        target_role=roadmap_dict["target_role"],
        duration_weeks=roadmap_dict["duration_weeks"],
        total_skills=roadmap_dict["total_skills"],
        weeks=roadmap_dict["weeks"],
        created_at=saved_rdm.created_at.isoformat() if saved_rdm.created_at else None
    )


@router.get("/{roadmap_id}", response_model=RoadmapResponse)
def get_roadmap_by_id(roadmap_id: str, db: Session = Depends(get_db)):
    """Retrieve full details and milestone checklist for a saved roadmap."""
    rec = db.query(SavedRoadmap).filter(SavedRoadmap.id == roadmap_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Roadmap not found.")

    data = json.loads(rec.roadmap_json)
    return RoadmapResponse(
        id=rec.id,
        title=rec.title,
        target_role=rec.target_role,
        duration_weeks=rec.duration_weeks,
        total_skills=data.get("total_skills", 0),
        weeks=data.get("weeks", []),
        created_at=rec.created_at.isoformat() if rec.created_at else None
    )


@router.post("/{roadmap_id}/toggle-task")
def toggle_task(
    roadmap_id: str,
    payload: TaskToggleRequest,
    db: Session = Depends(get_db)
):
    """Update task completion status in a roadmap."""
    rec = db.query(SavedRoadmap).filter(SavedRoadmap.id == roadmap_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Roadmap not found.")

    data = json.loads(rec.roadmap_json)
    updated = False
    for week in data.get("weeks", []):
        if week.get("week_number") == payload.week_number:
            for t in week.get("tasks", []):
                if t.get("id") == payload.task_id:
                    t["completed"] = payload.completed
                    updated = True
                    break

    if updated:
        rec.roadmap_json = json.dumps(data)
        db.commit()

    return {"status": "success", "task_id": payload.task_id, "completed": payload.completed}
