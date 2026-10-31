"""Skill Gap Analysis and Compatibility Evaluation API Routes."""

import json
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_optional
from app.models.profile import Profile
from app.models.job import JobPosting
from app.models.gap_analysis import SavedGapAnalysis
from app.schemas.gap import GapAnalysisRequest, GapAnalysisResponse
from app.agents.state import AgentState
from app.agents.graph import skillsync_workflow
from app.services.skill_extractor import extract_skills_from_text
from app.services.job_api_service import CURATED_BENCHMARK_JOBS

router = APIRouter(prefix="/gap", tags=["Skill Gap Analysis"])


@router.post("/analyze", response_model=GapAnalysisResponse)
def run_gap_analysis(
    payload: GapAnalysisRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_optional)
):
    """Execute LangGraph multi-agent workflow to compute compatibility and identify skill gaps."""
    # 1. Resolve candidate skills and profile
    candidate_skills = payload.candidate_skills or []
    candidate_name = payload.candidate_name or "Candidate"
    candidate_exp = payload.candidate_experience_years or 3.0

    if payload.profile_id:
        p = db.query(Profile).filter(Profile.id == payload.profile_id).first()
        if p:
            candidate_skills = json.loads(p.skills_json or "[]")
            candidate_name = p.name
            candidate_exp = p.experience_years
    elif payload.raw_resume_text:
        candidate_skills = extract_skills_from_text(payload.raw_resume_text, default_mandatory=False, is_job_posting=False)

    # 2. Resolve job specifications
    target_job = None
    job_title = payload.job_title or "Target Engineering Role"
    job_skills = []
    required_exp = payload.required_experience_years or 3.0

    if payload.job_id:
        db_job = db.query(JobPosting).filter(JobPosting.id == payload.job_id).first()
        if db_job:
            target_job = {
                "id": db_job.id,
                "title": db_job.title,
                "company": db_job.company,
                "description": db_job.description,
                "required_experience_years": db_job.required_experience_years,
            }
            job_title = db_job.title
            job_skills = json.loads(db_job.skills_json or "[]")
            required_exp = db_job.required_experience_years
        else:
            # Check curated benchmark
            for cj in CURATED_BENCHMARK_JOBS:
                if cj["id"] == payload.job_id:
                    target_job = cj
                    job_title = cj["title"]
                    job_skills = extract_skills_from_text(cj["description"], default_mandatory=True, is_job_posting=True)
                    required_exp = cj.get("required_experience_years", 3)
                    break
    elif payload.raw_job_description:
        job_skills = extract_skills_from_text(payload.raw_job_description, default_mandatory=True, is_job_posting=True)
        target_job = {
            "title": job_title,
            "description": payload.raw_job_description,
            "required_experience_years": required_exp
        }

    # 3. Assemble Agent State and run workflow graph
    initial_state = AgentState(
        session_id=str(uuid.uuid4()),
        candidate_profile={"name": candidate_name, "experience_years": candidate_exp},
        extracted_candidate_skills=candidate_skills,
        target_job=target_job,
        extracted_job_skills=job_skills,
    )

    final_state = skillsync_workflow.run(initial_state)

    gap_res = final_state.gap_analysis_result
    if not gap_res:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent workflow encountered an issue calculating the skill gap analysis."
        )

    # 4. Save analysis record to database
    analysis_id = f"gap-{uuid.uuid4().hex[:10]}"
    saved_run = SavedGapAnalysis(
        id=analysis_id,
        user_id=user["sub"],
        profile_id=payload.profile_id,
        job_id=payload.job_id,
        job_title=job_title,
        candidate_name=candidate_name,
        overall_score=gap_res["overall_score"],
        mandatory_score=gap_res["mandatory_score"],
        preferred_score=gap_res["preferred_score"],
        experience_score=gap_res["experience_score"],
        alignment_tier=gap_res["alignment_tier"],
        result_json=json.dumps(gap_res)
    )
    db.add(saved_run)
    db.commit()

    return GapAnalysisResponse(
        id=analysis_id,
        overall_score=gap_res["overall_score"],
        mandatory_score=gap_res["mandatory_score"],
        preferred_score=gap_res["preferred_score"],
        experience_score=gap_res["experience_score"],
        alignment_tier=gap_res["alignment_tier"],
        executive_summary=gap_res["executive_summary"],
        disclaimer=gap_res["disclaimer"],
        counts=gap_res["counts"],
        matched_skills=gap_res["matched_skills"],
        partially_matched_skills=gap_res["partially_matched_skills"],
        missing_mandatory_skills=gap_res["missing_mandatory_skills"],
        missing_preferred_skills=gap_res["missing_preferred_skills"],
        unverified_skills=gap_res["unverified_skills"],
        category_breakdown=gap_res["category_breakdown"],
        audit_trail=final_state.audit_trail,
        provider_info=final_state.provider_info
    )


@router.get("/history")
def get_user_gap_history(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_optional)
):
    """Retrieve previous gap analysis runs for this user."""
    runs = db.query(SavedGapAnalysis).filter(SavedGapAnalysis.user_id == user["sub"]).order_by(SavedGapAnalysis.created_at.desc()).limit(15).all()
    history = []
    for r in runs:
        history.append({
            "id": r.id,
            "job_title": r.job_title,
            "candidate_name": r.candidate_name,
            "overall_score": r.overall_score,
            "mandatory_score": r.mandatory_score,
            "preferred_score": r.preferred_score,
            "alignment_tier": r.alignment_tier,
            "created_at": r.created_at.isoformat() if r.created_at else None
        })
    return history


@router.get("/{analysis_id}", response_model=GapAnalysisResponse)
def get_gap_analysis_by_id(analysis_id: str, db: Session = Depends(get_db)):
    """Retrieve full details of a saved gap analysis."""
    rec = db.query(SavedGapAnalysis).filter(SavedGapAnalysis.id == analysis_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Gap analysis record not found.")

    res = json.loads(rec.result_json)
    return GapAnalysisResponse(
        id=rec.id,
        overall_score=rec.overall_score,
        mandatory_score=rec.mandatory_score,
        preferred_score=rec.preferred_score,
        experience_score=rec.experience_score,
        alignment_tier=rec.alignment_tier,
        executive_summary=res.get("executive_summary", ""),
        disclaimer=res.get("disclaimer", ""),
        counts=res.get("counts", {}),
        matched_skills=res.get("matched_skills", []),
        partially_matched_skills=res.get("partially_matched_skills", []),
        missing_mandatory_skills=res.get("missing_mandatory_skills", []),
        missing_preferred_skills=res.get("missing_preferred_skills", []),
        unverified_skills=res.get("unverified_skills", []),
        category_breakdown=res.get("category_breakdown", [])
    )
