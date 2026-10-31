"""Job Search and Ingestion API Routes."""

import json
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.job import JobPosting
from app.schemas.job import JobOut, PasteJobRequest
from app.services.job_api_service import CURATED_BENCHMARK_JOBS, search_all_jobs
from app.services.skill_extractor import extract_skills_from_text

router = APIRouter(prefix="/jobs", tags=["Job Intelligence"])


@router.get("/search", response_model=List[JobOut])
def search_jobs(
    query: str = Query(default="", description="Role or skill keywords (e.g., Python, AI, React)"),
    location: str = Query(default="", description="Location filter (e.g., Remote, US)"),
    source: str = Query(default="all", description="Source: 'all', 'remotive', 'arbeitnow', 'curated'")
):
    """Search job postings across live feeds (Remotive, Arbeitnow) and benchmark repositories."""
    jobs = search_all_jobs(query=query, location=location, source=source)
    response_list = []
    for j in jobs:
        response_list.append(JobOut(
            id=j["id"],
            title=j["title"],
            company=j.get("company", "Tech Company"),
            location=j.get("location", "Remote"),
            source=j.get("source", "Remote API"),
            salary_range=j.get("salary_range"),
            required_experience_years=j.get("required_experience_years", 3),
            description=j.get("description", ""),
            url=j.get("url"),
            extracted_skills=j.get("extracted_skills", []),
            skills_count=len(j.get("extracted_skills", []))
        ))
    return response_list


@router.post("/paste", response_model=JobOut)
def paste_job_description(payload: PasteJobRequest, db: Session = Depends(get_db)):
    """Manually paste a raw job description, run skill extraction, and persist."""
    extracted = extract_skills_from_text(payload.description, default_mandatory=True, is_job_posting=True)

    job_id = f"job-{uuid.uuid4().hex[:10]}"
    new_job = JobPosting(
        id=job_id,
        title=payload.title,
        company=payload.company,
        location=payload.location,
        source="manual_paste",
        salary_range=payload.salary_range or "Competitive",
        required_experience_years=payload.required_experience_years or 3,
        description=payload.description,
        skills_json=json.dumps(extracted)
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return JobOut(
        id=new_job.id,
        title=new_job.title,
        company=new_job.company,
        location=new_job.location,
        source=new_job.source,
        salary_range=new_job.salary_range,
        required_experience_years=new_job.required_experience_years,
        description=new_job.description,
        extracted_skills=extracted,
        skills_count=len(extracted)
    )


@router.get("/benchmark", response_model=List[JobOut])
def get_benchmark_jobs():
    """Retrieve pre-verified benchmark jobs for AI Engineer, Fullstack, DevOps, and Data Science."""
    results = []
    for j in CURATED_BENCHMARK_JOBS:
        skills = extract_skills_from_text(j["description"], default_mandatory=True, is_job_posting=True)
        results.append(JobOut(
            id=j["id"],
            title=j["title"],
            company=j["company"],
            location=j["location"],
            source=j["source"],
            salary_range=j["salary_range"],
            required_experience_years=j["required_experience_years"],
            description=j["description"],
            extracted_skills=skills,
            skills_count=len(skills)
        ))
    return results


@router.get("/{job_id}", response_model=JobOut)
def get_job_by_id(job_id: str, db: Session = Depends(get_db)):
    """Retrieve details and extracted specifications for a specific job."""
    # First check database
    db_job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if db_job:
        skills = json.loads(db_job.skills_json or "[]")
        return JobOut(
            id=db_job.id,
            title=db_job.title,
            company=db_job.company,
            location=db_job.location,
            source=db_job.source,
            salary_range=db_job.salary_range,
            required_experience_years=db_job.required_experience_years,
            description=db_job.description,
            extracted_skills=skills,
            skills_count=len(skills)
        )

    # Next check curated benchmark
    for cj in CURATED_BENCHMARK_JOBS:
        if cj["id"] == job_id:
            skills = extract_skills_from_text(cj["description"], default_mandatory=True, is_job_posting=True)
            return JobOut(
                id=cj["id"],
                title=cj["title"],
                company=cj["company"],
                location=cj["location"],
                source=cj["source"],
                salary_range=cj["salary_range"],
                required_experience_years=cj["required_experience_years"],
                description=cj["description"],
                extracted_skills=skills,
                skills_count=len(skills)
            )

    raise HTTPException(status_code=404, detail="Job posting not found.")
